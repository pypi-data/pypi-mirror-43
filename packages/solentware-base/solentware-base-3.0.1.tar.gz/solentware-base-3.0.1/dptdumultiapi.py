# dptdumultiapi.py
# Copyright (c) 2007, 2009 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""DPT multi-step deferred update version.

A database API for bulk insertion of records, implemented using dptdb,
where indicies are represented as lists or bitmaps of record numbers.
    
dptdb is an interface to DPT's database engine generated by Swig.

DPT is an emulation of Model 204 version 5 which runs on Microsoft Windows.

You should use the single-step deferred update mode in the dptduapi module.

DPT kept the multi-step deferred update mode for backward compatibility when
single-step deferred update mode was added.

DPT provides several options for multi-step deferred update.  This module
supports the NoPad with NoCRLF option.

This module on Windows and Wine only.

See www.dptoolkit.com for details of DPT.

At present this module does not work because it uses the class definition:

class _rmFile(file)

where 'file' is the class removed from Python ages ago.

This module has survived as an example of how to code multi-step in Python.

"""

from .api.database import DatabaseError

import sys
if sys.platform != 'win32':
    raise DatabaseError('Platform is not "win32"')
del sys
del DatabaseError

import os
import os.path
from heapq import heapify, heappop, heappush
import io

from dptdb import dptapi

from . import dptduapi
from .api.constants import (ORD, ONM, DPT_DEFER_FOLDER, TAPEA, TAPEN)

DU_AUDIT_LINE = 'DU'

# Number of bytes read from DPT sequential file before writing sorted chunks.
# 25000000 is reasonable on XP running in 500Mb where average value length in
# field=value pairs for ordered fields is something like 10-15 bytes. The Peak
# Commit Charge reported by Task Manager is 537Mb. Setting DEFAULT_SEQFILE_READ
# to 100000000 gives a peak of about 850Mb and significant disk activity
# judging by disk activity LED.
DEFAULT_SEQFILE_READ = 25000000

# Number of bytes read from merged sorted chunk file for a field when building
# input file for DPT API ApplyDeferredUpdataes() call
DEFAULT_CHUNK_READ = 10000000


class DPTdumultiapiError(dptduapi.DPTduapiError):
    pass


class DPTdumultiapi(dptduapi.DPTduapi):
    
    """Bulk insert to database in DPTfolder using database_specification.

    A default subfolder in DPTfolder is used for deferred updates when
    dferfolder is None.

    Support the NoPad with NoCRLF multi-step deferred update option on DPT.

    DPT single-step deferred update methods provided by the dptduapi.DPTduapi
    superclass are overridden here.

    """
    
    def __init__(self,
                 database_specification,
                 DPTfolder,
                 deferfolder=None,
                 **kargs):
        """Create DPT multi-step deferred update environment."""
        super(DPTdumultiapi, self).__init__(
            database_specification, DPTfolder, **kargs)

        if deferfolder is None:
            deferfolder = DPT_DEFER_FOLDER
        try:
            self._deferfolder = os.path.abspath(
                os.path.join(DPTfolder, deferfolder))
        except:
            msg = ' '.join(['Defer update folder name', str(deferfolder),
                            'is not valid'])
            raise DPTdumultiapiError(msg)
        
        #Files to be updated in multi-step deferred update mode
        self._deferupdatefiles = kargs.get('deferupdatefiles', dict())
        for duf in self._deferupdatefiles:
            if duf not in self.database_definition:
                msg = ' '.join(['File name', str(duf),
                                'is not a file specified for database'])
                raise DPTdumultiapiError(msg)
        
    def close_context(self):
        """Close all DPT files and multi-step specific sequential files."""
        if self.dbservices is None:
            return
        for dd in self.database_definition:
            self.database_definition[dd].close(self.dbservices,
                                               self.get_sfserv())

    def do_deferred_updates(self):
        """Apply deferred updates."""
        for dd in self._deferupdatefiles:
            self.database_definition[dd].do_nopad_noCRLF_deferred_updates(
                self.dbservices, self._deferfolder)
        try:
            os.rmdir(self._deferfolder)
        except:
            pass

    #def make_root(self, name, fname, dptfile, fieldnamefn, sfi):
    #    """DPT file interface customised for multi-step deferred update"""
    #    return DPTRecord(name, fname, dptfile, fieldnamefn, sfi)

    def make_root(self, **kw):
        """DPT file interface customised for multi-step deferred update"""
        return DPTRecord(**kw)

    def open_context_allocated(self, files=()):
        """Open all files in multi-step deferred update mode.

        Intended use is to open files to examine file status, or perhaps the
        equivalent of DPT command VIEW TABLES, when the database is closed as
        far as the application subclass of dptbase.Database is concerned.

        It is assumed that the Database Services object exists and that an
        earlier call to OpenContext_DUMulti has been made.

        """
        # It is assumed a call to OpenContext_DUMulti was made earlier.
        for dd in files:
            if dd in self.database_definition:
                root = self.database_definition[dd]
                self.dbservices.Allocate(
                    root._ddname,
                    root._file,
                    dptapi.FILEDISP_OLD)
                cs = dptapi.APIContextSpecification(root._ddname)
                # It is wrong to call OpenContext_DUMulti here, even if it has
                # not been called earlier.
                root._opencontext = self.dbservices.OpenContext(cs)


class _DPTdumultiDeferBase(object):
    
    """Sort sequential file containing deferred updates.

    This class, and subclasses, merge the sorted sequential files output
    during do_nopad_noCRLF_deferred_updates processing into two files that will
    be processed by ApplyDeferredUpdates (DPT API) to update the database.

    _DPTdumultiDeferBase supports deferred updates for a field on a file.
    Note that self._dptfieldid is set in DPTRecord.open_root().
    This class should not be used directly. Use the appropriate
    subclass instead. The attributes and methods in this class are
    used by more than one, but not necessarily all, subclasses.
    
    """
    
    def __init__(self):
        super(_DPTdumultiDeferBase, self).__init__()
        self._dptfieldid = None
        self._fid = None
        self._ordered = None
        self._ordnum = None

    def set_field_identity(self, field_identity, ordered, ordnum):
        """Copy field details to instance"""
        self._dptfieldid = field_identity
        fidhigh, fidlow = divmod(field_identity, 256)
        self._fid = chr(fidlow) + chr(fidhigh)
        self._ordered = ordered
        self._ordnum = ordnum


    def unset_sort_index(self):
        """Clear field details from instance."""
        self._dptfieldid = None
        self._fid = None
        self._ordered = None
        self._ordnum = None


#Probably no need for this class to be separate from its base class any more
#as NoPad NoCRLF is only supported deferred update file format
class _DPTdumultiNoPadNoCRLF(_DPTdumultiDeferBase):
    
    """Sort sequential file containing deferred updates in NOPAD|NOCRLF format.

    This class reads a sequential file; sorts the records; and writes the
    result to a series of sequential files, one per field, which are then
    read in parallel to update the the DPT database.
    
    """

    def __init__(self):
        """Extend _DPTdumultiDeferBase with sort control structures."""
        super(_DPTdumultiNoPadNoCRLF, self).__init__()
        self.deferbuffer = []
        self.dufolder = None
        self.cyclecount = 0  #count sequential files created while sorting

    def delete_sort_file(self, sortfile):
        """Delete processed file created while sorting."""
        try:
            sortfile.close()
            os.remove(sortfile.name)
        except:
            pass
        
    def get_input_files(self):
        """Open all files created while sorting."""
        return [_rmFile(os.path.join(self.dufolder, f), 'rb')
                for f in os.listdir(self.dufolder) if f.isdigit()]

    def get_new_serial_file(self):
        """Open and return next file in filename series."""
        self.cyclecount += 1
        return _rmFile(
            os.path.join(
                self.dufolder,
                str(self.cyclecount)),
            'wb')

    def merge_defer_folder_files(self, GetNextRecord):
        """Merge sorted chunk files for processing by ApplyDeferredUpdates.

        The sources are merged 256 chunks at a time until there is only one
        chunk file.  It is wise to limit the number of files needed open at
        the same time but this number chosen to match the number used by DPT
        in the single-step deferred update.

        """
        # Function insort from module bisect is an alternative to the functions
        # from module heapq. It may be better.
        sources = self.get_input_files()

        while len(sources) > 1:
            outfile = self.get_new_serial_file()
            record = []
            heapify(record)
            for f in sources[:256]:
                r = GetNextRecord(f)
                if r is None:
                    del sources[sources.index(f)]
                    self.delete_sort_file(f)
                else:
                    heappush(record, (r, f))
            more = len(record) > 0
            while more:
                wr, f = heappop(record)
                outfile.write(wr[-1])
                r = GetNextRecord(f)
                if r is None:
                    del sources[sources.index(f)]
                    self.delete_sort_file(f)
                    more = len(record) > 0
                else:
                    heappush(record, (r, f))
            outfile.close()
            sources.append(_rmFile(
                os.path.join(
                    self.dufolder,
                    str(self.cyclecount)),
                'rb'))

    def set_defer_folder(self, dufolder):
        """Set defer update folder."""
        self.dufolder = dufolder

    def write_chunk(self):
        """Sort the deferred updates and write to chunk file."""
        self.deferbuffer.sort()
        outfile = self.get_new_serial_file()
        try:
            for r in self.deferbuffer:
                outfile.write(r[-1])
        finally:
            outfile.close()
        self.deferbuffer[:] = []

    def write_merged_files_to_seqfile(self, outfile):
        """Copy merged chunk file to input file for ApplyDeferredUpdates.

        The merged chunk file is assumed to be sorted through generation by
        the merge_defer_folder_files method.

        """
        f = _rmFile(
            os.path.join(
                self.dufolder,
                str(self.cyclecount)),
            'rb')
        r = f.read(DEFAULT_CHUNK_READ)
        while len(r) > 0:
            outfile.write(r)
            r = f.read(DEFAULT_CHUNK_READ)
        self.delete_sort_file(f)


class _DPTdumultiNoPadNoCRLFOrdChar(_DPTdumultiNoPadNoCRLF):
    
    """Customise _DPTdumultiNoPadNoCRLF to handle Ordered Character data.
    """

    def merge_defer_folder_files(self):
        """Merge alpha sources for processing by ApplyDeferredUpdates."""
        super(_DPTdumultiNoPadNoCRLFOrdChar, self).merge_defer_folder_files(
            _rmFile.read_nopad_noCRLF_ord_char)


class _DPTdumultiNoPadNoCRLFOrdNum(_DPTdumultiNoPadNoCRLF):
    
    """Customise _DPTdumultiNoPadNoCRLF to handle Ordered Numeric data.
    """

    def merge_defer_folder_files(self):
        """Merge numeric sources for processing by ApplyDeferredUpdates."""
        super(_DPTdumultiNoPadNoCRLFOrdNum, self).merge_defer_folder_files(
            _rmFile.read_nopad_noCRLF_ord_num)


class DPTRecord(dptduapi.DPTRecord):

    """Provide multi-step deferred update sort processing for DPT file.

    This class implements methods to sort the sequential files created
    when adding records to a file in deferred update mode and applies the
    sorted indexes by calling the DPT API method ApplyDeferredUpdates.
    
    """

    _defer_read_limit = DEFAULT_SEQFILE_READ
    
    #def __init__(self, name, fname, dptdesc, fieldnamefn, sfi):
    def __init__(self, sfi=None, **kw):
        """Extend to include deferred update sequential file definition"""
        #super().__init__(
        #    name,
        #    fname,
        #    dptdesc,
        #    fieldnamefn,
        #    sfi)
        super().__init__(**kw)
        
        self._seqfileid = sfi
        self._dufields = []
        self._seqfilealpha = ''.join(('SFA', str(self._seqfileid)))
        self._seqfilenumeric = ''.join(('SFN', str(self._seqfileid)))
        self._seqfilealphasorted = ''.join(('SFAS', str(self._seqfileid)))
        self._seqfilenumericsorted = ''.join(('SFNS', str(self._seqfileid)))
        self._duclass = dict()
        for s in self.secondary:
            self._duclass[s] = None

        #Flag controlling deferred update OpenContext calls.
        self._dumulti_called = False

    def close(self, dbserv, sfserv):
        """Extend close to Free the sequential files."""
        super().close(dbserv)
        try:
            sfserv.Free(self._seqfilealpha)
        except:
            pass
        try:
            sfserv.Free(self._seqfilenumeric)
        except:
            pass

    def do_nopad_noCRLF_deferred_updates(self, dbserv, dbfolder):
        """Apply deferred updates from NOPAD|NOCRLF sequential files.
        
        folder contains a folder for each (DD) file with deferred updates and
        is used for temporary files while sorting the sequential files.
        The (DD) files are left closed (in non-deferred mode) on completion.
        
        The sequential files used to sort the deferred updates can be very
        large so each file is deleted as soon as possible after this method
        no longer needs the file.  This means there is less scope for
        restarting a failed run from a completed intermediate stage.
        """
        sfserv = dbserv.SeqServs()
        
        self.close(dbserv, sfserv)

        defer = dict()
        for s in self._duclass:
            defer[self._duclass[s]._fid] = self._duclass[s]
            
        dbserv.Core().AuditLine(
            ' '.join((
                'Split deferred update sequential files for file',
                repr(self._fd_name),
                'into sorted files for each field')),
            DU_AUDIT_LINE)

        infile = _rmFile(
            os.path.join(
                os.path.dirname(self._file),
                ''.join((self._seqfilealpha, '.txt'))),
            'rb')
        try:
            marker = 0
            chunk_number = 0
            d = infile.read_nopad_noCRLF_ord_char()
            while d:
                defer[d[-3]].deferbuffer.append(d)
                if infile.tell() - marker > self._defer_read_limit:
                    for fid in defer:
                        if isinstance(
                            defer[fid], _DPTdumultiNoPadNoCRLFOrdChar):
                            defer[fid].write_chunk()
                    marker = infile.tell()
                    dbserv.Core().AuditLine(
                        ' '.join((
                            'Chunk',
                            str(chunk_number),
                            'written for all ordered character fields',
                            'in deferred update mode')),
                        DU_AUDIT_LINE)
                    chunk_number += 1
                d = infile.read_nopad_noCRLF_ord_char()
        finally:
            infile.close()
    
        infile = _rmFile(
            os.path.join(
                os.path.dirname(self._file),
                ''.join((self._seqfilenumeric, '.txt'))),
            'rb')
        try:
            marker = 0
            chunk_number = 0
            d = infile.read_nopad_noCRLF_ord_num()
            while d:
                defer[d[-3]].deferbuffer.append(d)
                if infile.tell() - marker > self._defer_read_limit:
                    for fid in defer:
                        if isinstance(
                            defer[fid], _DPTdumultiNoPadNoCRLFOrdNum):
                            defer[fid].write_chunk()
                    marker = infile.tell()
                    dbserv.Core().AuditLine(
                        ' '.join((
                            'Chunk',
                            str(chunk_number),
                            'written for all ordered numeric fields',
                            'in deferred update mode')),
                        DU_AUDIT_LINE)
                    chunk_number += 1
                d = infile.read_nopad_noCRLF_ord_num()
        finally:
            infile.close()

        for fid in defer:
            defer[fid].write_chunk()
        dbserv.Core().AuditLine(
            ' '.join((
                'Final chunks',
                'written for all ordered fields',
                'in deferred update mode')),
            DU_AUDIT_LINE)
        
        for f in (self._seqfilealpha, self._seqfilenumeric):
            try:
                os.remove(
                    os.path.join(
                        os.path.dirname(self._file),
                        ''.join((f, '.txt'))))
            except:
                pass

        dbserv.Core().AuditLine(
            ' '.join((
                'Merge sorted files for each field on file',
                repr(self._fd_name),
                'into two sorted sequential files (char and num)')),
            DU_AUDIT_LINE)

        outfilealpha = open(
            os.path.join(
                os.path.dirname(self._file),
                ''.join((self._seqfilealphasorted, '.txt'))),
            'wb')
        outfilenumeric = open(
            os.path.join(
                os.path.dirname(self._file),
                ''.join((self._seqfilenumericsorted, '.txt'))),
            'wb')

        for d in self._duclass:
            dbserv.Core().AuditLine(
                ' '.join((
                    'Merge sorted files for field', repr(d),
                    'on file', repr(self._fd_name))),
                DU_AUDIT_LINE)

            if self._fields[self.secondary[d]][ONM]:
                self._duclass[d].merge_defer_folder_files()
            elif self._fields[self.secondary[d]][ORD]:
                self._duclass[d].merge_defer_folder_files()

            if self._fields[self.secondary[d]][ONM]:
                self._duclass[d].write_merged_files_to_seqfile(outfilenumeric)
            elif self._fields[self.secondary[d]][ORD]:
                self._duclass[d].write_merged_files_to_seqfile(outfilealpha)

        outfilealpha.close()
        outfilenumeric.close()

        dbserv.Core().AuditLine(
            ' '.join((
                'Merge sorted files for file',
                repr(self._fd_name), 'completed')),
            DU_AUDIT_LINE)

        deferfolder = os.path.join(dbfolder, self._ddname)
                    
        for s in self._dufields:
            f = self.secondary[s]
            dufolder = os.path.join(deferfolder, f)
            try:
                os.rmdir(dufolder)
            except:
                pass

        try:
            os.rmdir(deferfolder)
        except:
            pass

        dbserv.Allocate(
            self._ddname,
            self._file,
            dptapi.FILEDISP_COND)
        sfserv.Allocate(
            TAPEN,
            os.path.join(
                os.path.dirname(self._file),
                ''.join((self._seqfilenumericsorted, '.txt'))),
            dptapi.FILEDISP_OLD)
        sfserv.Allocate(
            TAPEA,
            os.path.join(
                os.path.dirname(self._file),
                ''.join((self._seqfilealphasorted, '.txt'))),
            dptapi.FILEDISP_OLD)
        cs = dptapi.APIContextSpecification(self._ddname)
        self._opencontext = dbserv.OpenContext(cs)

        self._opencontext.ApplyDeferredUpdates(0)

        self.close(dbserv, sfserv)
        sfserv.Free(TAPEA)
        sfserv.Free(TAPEN)
        for f in (self._seqfilealphasorted,
                  self._seqfilenumericsorted):
            os.remove(
                os.path.join(
                    os.path.dirname(self._file),
                    ''.join((f, '.txt'))))

        for d in self._duclass:
            self._duclass[d].unset_sort_index()

        for s in self.secondary:
            self._duclass[s] = None

    def open_root(self, db):
        """Extend to open file in multi-step mode.

        Create folders to hold the temporary files used in sort and merge.
        Call DPT API OpenContext_DUMulti method to open file in deferred
        update mode if this method has not been used before in this run.
        Otherwise call OpenContext which does the same thing because the
        deferred update state is preserved from earlier.  The sequential
        files must be allocated FILEDISP_MOD once they exist to avoid
        losing the existing content.  See DPT documentation for full
        detail.

        """
        if self._fd_name not in db._deferupdatefiles:
            return

        super(dptduapi.DPTRecord, self).open_root(db)

        #get list of fields whose updates can be deferred
        self._dufields = []
        for s in self.secondary:
            f = self.secondary[s]
            if self._fields[f][ORD]:
                self._dufields.append(s)
            if self._fields[f][ONM]:
                self._dufields.append(s)
        if not self._dufields:
            return
        
        try:
            os.mkdir(db._deferfolder)
        except:
            pass
        
        deferfolder = os.path.join(
            db._deferfolder, self._ddname) 
        try:
            os.mkdir(deferfolder)
        except:
            pass
            
        for s in self._dufields:
            dudefer = None
            f = self.secondary[s]
            if self._fields[f][ONM]:
                dudefer = _DPTdumultiNoPadNoCRLFOrdNum
            elif self._fields[f][ORD]:
                dudefer = _DPTdumultiNoPadNoCRLFOrdChar
            if dudefer:
                self._duclass[s] = self._make_DUclass(dudefer)
                dufolder = os.path.join(deferfolder, f)
                self._duclass[s].set_defer_folder(dufolder)
                try:
                    os.mkdir(dufolder)
                except:
                    pass
            else:
                self._duclass[s] = None

        db.dbservices.Allocate(
            self._ddname,
            self._file,
            dptapi.FILEDISP_COND)

        sfserv = db.dbservices.SeqServs()
        for f in (self._seqfilealpha, self._seqfilenumeric):
            fullpath = os.path.join(
                os.path.dirname(self._file),
                ''.join((f, '.txt')))
            # MOD once file exists so existing updates are not discarded
            if os.path.exists(fullpath):
                filedisp = dptapi.FILEDISP_MOD
            else:
                filedisp = dptapi.FILEDISP_COND
            sfserv.Allocate(f, fullpath, filedisp)

        cs = dptapi.APIContextSpecification(self._ddname)
        # First call in run must be OpenContext_DUMulti and rest OpenContext
        if self._dumulti_called:
            self._opencontext = db.dbservices.OpenContext(cs)
        else:
            self._dumulti_called = True
            self._opencontext = db.dbservices.OpenContext_DUMulti(
                cs,
                self._seqfilenumeric,
                self._seqfilealpha,
                -1,
                dptapi.DU_FORMAT_NOCRLF | dptapi.DU_FORMAT_NOPAD)

        fac = self._opencontext.OpenFieldAttCursor()
        while fac.Accessible():
            name = dptapi.StdStringPtr()
            name.assign(fac.Name())
            fn = name.value()
            fid = fac.FID()
            atts = fac.Atts()
            for s in self.secondary:
                if fn == self.secondary[s]:
                    self._duclass[s].set_field_identity(
                        fid,
                        atts.IsOrdered(),
                        atts.IsOrdNum())
            fac.Advance(1)
        self._opencontext.CloseFieldAttCursor(fac)

    def reset_defer_limit(self):
        """Set defer record limit to default class limit"""
        self.set_defer_limit(DPTRecord._defer_read_limit)

    def set_defer_limit(self, limit):
        """Set defer record limit for comparison with record number."""
        self._defer_read_limit = limit

    def _make_DUclass(self, duclass):
        """Return a file reader class.

        Where duclass is one of the classes provided by this module return
        an instance of the class.  Otherwise build a new class with dulass
        and _DPTdumultiNoPadNoCRLFOrdChar as superclasses and return an
        instance of this new class.

        """
        if duclass in (
            _DPTdumultiNoPadNoCRLFOrdChar,
            _DPTdumultiNoPadNoCRLFOrdNum,
            ):
            return duclass()
        else:
            class DU(duclass, _DPTdumultiNoPadNoCRLFOrdChar):
                def __init__(self):
                    super(DU, self).__init__()
            return DU()


# Definition was 'class _rmFile(file):' from Python 2 days and not updated till
# November 2018 because multi-step became obsolete long ago.  Single-step is at
# least 20 times quicker.
# Minimal changes made to use io.FileIO as base class instead.
class _rmFile(io.FileIO):

    """Extend file to support formats used in deferred update sequential files.
    
    Cheaper to reverse the record number string where necessary than call
    a casting method via SWIG. Can do this because sort order is same.
    Must call a casting method for RoundedDouble because the sort order
    of the string cast and the RoundedDouble cast is not the same.
    
    """

    def __init__(self, filename, mode='r', bufsize=-1):
        """See Python manual."""
        super(_rmFile, self).__init__(filename, mode, bufsize)
        self._roundeddouble = dptapi.APIRoundedDouble()
        self._CastToRoundedDouble = self._roundeddouble.pyCastToRoundedDouble

    def read_nopad_noCRLF_ord_char(self):
        """Return one record decorated for sorting or None"""
        recno = self.read(4)
        fid = self.read(2)
        valuelen = self.read(1)
        try:
            value = self.read(ord(valuelen))
        except TypeError:
            if len(recno):
                raise
            else:
                return None
        except:
            raise
        recno = recno.decode('iso8859-1')
        fid = fid.decode('iso8859-1')
        value = value.decode('iso8859-1')
        return (value,
                recno[::-1],
                fid,
                ord(valuelen),
                ''.join((recno,
                         fid,
                         valuelen.decode('iso8859-1'),
                         value)).encode('iso8859-1'))

    def read_nopad_noCRLF_ord_num(self):
        """Return one record decorated for sorting or None"""
        recno = self.read(4)
        fid = self.read(2)
        valuelen = self.read(1)
        try:
            value = self.read(ord(valuelen))
        except TypeError:
            if len(recno):
                raise
            else:
                return None
        except:
            raise
        recno = recno.decode('iso8859-1')
        fid = fid.decode('iso8859-1')
        value = value.decode('iso8859-1')
        #Assign(0) raised an exception at one time. Remove try soon.
        try:
            self._roundeddouble.Assign(value)
        except:
            if value == 0:
                self._roundeddouble.Assign(0)
            else:
                raise
        return (self._roundeddouble.Data(),
                recno[::-1],
                fid,
                ord(valuelen),
                ''.join((recno,
                         fid,
                         valuelen.decode('iso8859-1'),
                         value)).encode('iso8859-1'))

