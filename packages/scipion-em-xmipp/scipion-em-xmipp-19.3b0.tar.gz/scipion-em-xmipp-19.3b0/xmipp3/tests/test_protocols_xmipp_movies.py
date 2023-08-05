# **************************************************************************
# *
# * Authors:    Laura del Cano (ldelcano@cnb.csic.es)
# *             Josue Gomez Blanco (josue.gomez-blanco@mcgill.ca)
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

from os.path import abspath
from pyworkflow.tests import *

from xmipp3.convert import *
from xmipp3.protocols import *
from pyworkflow.em.protocol import ProtImportMovies
import pyworkflow.utils as pwutils
from pyworkflow.em.protocol import ProtImportCoordinates

# Some utility functions to import movies that are used in several tests.
class TestXmippBase(BaseTest):
    @classmethod
    def setData(cls):
        cls.dataset = DataSet.getDataSet('movies')
        cls.movie1 = cls.dataset.getFile('qbeta/qbeta.mrc')
        cls.movie2 = cls.dataset.getFile('cct/cct_1.em')
    
    @classmethod
    def runImportMovie(cls, pattern, samplingRate, voltage, scannedPixelSize,
                       magnification, sphericalAberration, dosePerFrame=None):
        """ Run an Import micrograph protocol. """

        kwargs = {
                 'filesPath': pattern,
                 'magnification': magnification,
                 'voltage': voltage,
                 'sphericalAberration': sphericalAberration,
                 'dosePerFrame' : dosePerFrame
                  }

        # We have two options: pass the SamplingRate or
        # the ScannedPixelSize + microscope magnification
        if samplingRate is not None:
            kwargs.update({'samplingRateMode': 0,
                           'samplingRate': samplingRate})
        else:
            kwargs.update({'samplingRateMode': 1,
                           'scannedPixelSize': scannedPixelSize})

        cls.protImport = cls.newProtocol(ProtImportMovies, **kwargs)
        cls.proj.launchProtocol(cls.protImport, wait=True)

        if cls.protImport.isFailed():
            raise Exception("Protocol has failed. Error: ",
                            cls.protImport.getErrorMessage())

        # Check that input movies have been imported (a better way to do this?)
        if cls.protImport.outputMovies is None:
            raise Exception('Import of movies: %s, failed, '
                            'outputMovies is None.' % pattern)

        return cls.protImport
    
    @classmethod
    def runImportMovie1(cls, pattern):
        """ Run an Import movie protocol. """
        return cls.runImportMovie(pattern, samplingRate=1.14, voltage=300,
                                  sphericalAberration=2.26, dosePerFrame=1.5,
                                  scannedPixelSize=None, magnification=50000)
    
    @classmethod
    def runImportMovie2(cls, pattern):
        """ Run an Import movie protocol. """
        return cls.runImportMovie(pattern, samplingRate=1.4, voltage=300,
                                  sphericalAberration=2.7, dosePerFrame=1.5,
                                  scannedPixelSize=None,
                                  magnification=61000)


class TestOFAlignment(TestXmippBase):
    """This class check if the preprocessing micrographs protocol
    in Xmipp works properly."""

    @classmethod
    def setUpClass(cls):
        setupTestProject(cls)
        TestXmippBase.setData()
        cls.protImport1 = cls.runImportMovie1(cls.movie1)
        cls.protImport2 = cls.runImportMovie2(cls.movie2)
    
    def runOFProtocol(self, movies, label="Default", saveMic=True,
                      saveMovie=False, useAlign=False):
        protOF = XmippProtOFAlignment(doSaveAveMic=saveMic,
                                      doSaveMovie=saveMovie,
                                      useAlignment=useAlign)
        protOF.setObjLabel(label)
        protOF.inputMovies.set(movies)
        self.launchProtocol(protOF)
        return protOF
    
    def testAlignOF1(self):
        protOF1 = self.runOFProtocol(self.protImport1.outputMovies,
                                     label="Movie MRC")
        self.assertIsNotNone(protOF1.outputMicrographs,
                             "SetOfMicrographs has not been created.")
    
    def testAlignOF2(self):
        protOF2 = self.runOFProtocol(self.protImport2.outputMovies,
                                     label="Movie EM")
        self.assertIsNotNone(protOF2.outputMicrographs,
                             "SetOfMicrographs has not been created.")
    
    def testAlignOFSaveMovieAndMic(self):
        protOF3 = self.runOFProtocol(self.protImport1.outputMovies,
                                     label="Save Movie", saveMovie=True)
        self.assertIsNotNone(protOF3.outputMovies,
                             "SetOfMovies has not been created.")
    
    def testAlignOFSaveMovieNoMic(self):
        protOF4 = self.runOFProtocol(self.protImport1.outputMovies,
                                     label="Save Movie", saveMic=False,
                                     saveMovie=True)
        self.assertIsNotNone(protOF4.outputMovies,
                             "SetOfMovies has not been created.")
    
    def testAlignOFWAlignment(self):
        prot = XmippProtMovieCorr(doSaveAveMic=False)
        prot.inputMovies.set(self.protImport1.outputMovies)
        self.launchProtocol(prot)
        
        protOF5 = self.runOFProtocol(prot.outputMovies,
                                     label="Movie w Alignment",
                                     saveMic=False, 
                                     saveMovie=True)
        self.assertIsNotNone(protOF5.outputMovies,
                             "SetOfMovies has not been created.")


class TestOFAlignment2(TestXmippBase):
    """This class check if the optical flow protocol in Xmipp works properly."""
    @classmethod
    def setUpClass(cls):
        setupTestProject(cls)
        cls.dsMovies = DataSet.getDataSet('movies')

    def getArgs(self, filesPath, pattern=''):
        return {'importFrom': ProtImportMovies.IMPORT_FROM_FILES,
                'filesPath': self.dsMovies.getFile(filesPath),
                'filesPattern': pattern,
                'amplitudConstrast': 0.1,
                'sphericalAberration': 2.,
                'voltage': 300,
                'samplingRate': 3.54,
                'dosePerFrame' : 2.0,
                }

    def _checkOutput(self, prot, args, moviesId=[], size=None, dim=None):
        movies = getattr(prot, 'outputMovies', None)
        self.assertIsNotNone(movies)
        self.assertEqual(movies.getSize(), size)

        for i, m in enumerate(movies):
            if moviesId:
                self.assertEqual(m.getObjId(), moviesId[i])
            self.assertAlmostEqual(m.getSamplingRate(),
                                   args['samplingRate'])
            a = m.getAcquisition()
            self.assertAlmostEqual(a.getVoltage(), args['voltage'])

            if dim is not None: # Check if dimensions are the expected ones
                x, y, n = m.getDim()
                self.assertEqual(dim, (x, y, n))

    def _importMovies(self):
        args = self.getArgs('ribo/', pattern='*movie.mrcs')

        # Id's should be set increasing from 1 if ### is not in the pattern
        protMovieImport = self.newProtocol(ProtImportMovies, **args)
        protMovieImport.setObjLabel('from files')
        self.launchProtocol(protMovieImport)

        self._checkOutput(protMovieImport, args, [1, 2, 3], size=3,
                          dim=(1950, 1950, 16))
        return protMovieImport

    def test_OpticalFlow(self):
        protMovieImport = self._importMovies()

        mc1 = self.newProtocol(XmippProtMovieCorr,
                               objLabel='CC (no-write)',
                               alignFrame0=2, alignFrameN=10,
                               useAlignToSum=True,
                               splineOrder=XmippProtMovieCorr.INTERP_CUBIC,
                               numberOfThreads=1)
        mc1.inputMovies.set(protMovieImport.outputMovies)
        self.launchProtocol(mc1)

        of1 = self.newProtocol(XmippProtOFAlignment,
                               objLabel='OF DW',
                               alignFrame0=2, alignFrameN=10,
                               useAlignment=True,
                               doApplyDoseFilter=True,
                               doSaveUnweightedMic=True,
                               numberOfThreads=1)
        of1.inputMovies.set(mc1.outputMovies)
        self.launchProtocol(of1)
        self.assertIsNotNone(of1.outputMicrographs,
                             "SetOfMicrographs has not been created.")
        self.assertIsNotNone(of1.outputMicrographsDoseWeighted,
                             "SetOfMicrographs with dose correction has not "
                             "been created.")


class TestCorrelationAlignment(BaseTest):
    @classmethod
    def setData(cls):
        cls.ds = DataSet.getDataSet('movies')

    @classmethod
    def runImportMovies(cls, pattern, **kwargs):
        """ Run an Import micrograph protocol. """
        # We have two options: passe the SamplingRate or
        # the ScannedPixelSize + microscope magnification
        params = {'samplingRate': 1.14,
                  'voltage': 300,
                  'sphericalAberration': 2.7,
                  'magnification': 50000,
                  'scannedPixelSize': None,
                  'filesPattern': pattern
                  }
        if 'samplingRate' not in kwargs:
            del params['samplingRate']
            params['samplingRateMode'] = 0
        else:
            params['samplingRateMode'] = 1

        params.update(kwargs)

        protImport = cls.newProtocol(ProtImportMovies, **params)
        cls.launchProtocol(protImport)
        return protImport

    @classmethod
    def setUpClass(cls):
        setupTestProject(cls)
        cls.setData()
        cls.protImport1 = cls.runImportMovies(cls.ds.getFile('qbeta/qbeta.mrc'),
                                              magnification=50000)
        cls.protImport2 = cls.runImportMovies(cls.ds.getFile('cct/cct_1.em'),
                                              magnification=61000)

    def _checkMicrographs(self, protocol):
        self.assertIsNotNone(getattr(protocol, 'outputMicrographs', None),
                             "Output SetOfMicrographs were not created.")

    def _checkAlignment(self, movie, goldRange, goldRoi):
        alignment = movie.getAlignment()
        range = alignment.getRange()
        msgRange = "Alignment range must be %s (%s) and it is %s (%s)"
        self.assertEqual(goldRange, range, msgRange
                         % (goldRange, range, type(goldRange), type(range)))
        roi = alignment.getRoi()
        msgRoi = "Alignment ROI must be %s (%s) and it is %s (%s)"
        self.assertEqual(goldRoi, roi,
                         msgRoi % (goldRoi, roi, type(goldRoi), type(roi)))

    def test_qbeta_cpu(self):
        prot = self.newProtocol(XmippProtMovieCorr,doPSD=True, useGpu=False, doLocalAlignment=False)
        prot.inputMovies.set(self.protImport1.outputMovies)
        self.launchProtocol(prot)

        self._checkMicrographs(prot)
        self._checkAlignment(prot.outputMovies[1],
                             (1,7), [0, 0, 0, 0])

    def test_qbeta(self):
        prot = self.newProtocol(XmippProtMovieCorr,doPSD=True)
        prot.inputMovies.set(self.protImport1.outputMovies)
        self.launchProtocol(prot)

        self._checkMicrographs(prot)
        self._checkAlignment(prot.outputMovies[1],
                             (1,7), [0, 0, 0, 0])

    def test_qbeta_patches(self):
        prot = self.newProtocol(XmippProtMovieCorr,doPSD=True, patchX=7, patchY=7)
        prot.inputMovies.set(self.protImport1.outputMovies)
        self.launchProtocol(prot)

        self._checkMicrographs(prot)
        self._checkAlignment(prot.outputMovies[1],
                             (1,7), [0, 0, 0, 0])

    def test_qbeta_corrDownscale(self):
        prot = self.newProtocol(XmippProtMovieCorr,doPSD=True, corrDownscale=3)
        prot.inputMovies.set(self.protImport1.outputMovies)
        self.launchProtocol(prot)

        self._checkMicrographs(prot)
        self._checkAlignment(prot.outputMovies[1],
                             (1,7), [0, 0, 0, 0])

    def test_cct(self):
        prot = self.newProtocol(XmippProtMovieCorr,
                                doSaveMovie=True,
                                doPSD=True)
        prot.inputMovies.set(self.protImport2.outputMovies)
        self.launchProtocol(prot)

        self._checkMicrographs(prot)
        self._checkAlignment(prot.outputMovies[1],
                             (1,7), [0, 0, 0, 0])

    def test_qbeta_SkipCrop(self):
        prot = self.newProtocol(XmippProtMovieCorr,
                                alignFrame0=3, alignFrameN=5,
                                sumFrame0=3, sumFrameN=5,
                                cropOffsetX=10, cropOffsetY=10,
                                doPSD=True)
        prot.inputMovies.set(self.protImport1.outputMovies)
        self.launchProtocol(prot)

        self._checkMicrographs(prot)
        self._checkAlignment(prot.outputMovies[1],
                             (3,5), [10, 10, 0, 0])


class TestAverageMovie(BaseTest):
    @classmethod
    def setData(cls):
        cls.ds = DataSet.getDataSet('movies')

    @classmethod
    def runImportMovies(cls, pattern, **kwargs):
        """ Run an Import micrograph protocol. """
        # We have two options: passe the SamplingRate or
        # the ScannedPixelSize + microscope magnification
        params = {'samplingRate': 1.14,
                  'voltage': 300,
                  'sphericalAberration': 2.7,
                  'magnification': 50000,
                  'scannedPixelSize': None,
                  'filesPattern': pattern
                  }
        if 'samplingRate' not in kwargs:
            del params['samplingRate']
            params['samplingRateMode'] = 0
        else:
            params['samplingRateMode'] = 1

        params.update(kwargs)

        protImport = cls.newProtocol(ProtImportMovies, **params)
        cls.launchProtocol(protImport)
        return protImport

    @classmethod
    def setUpClass(cls):
        setupTestProject(cls)
        cls.setData()
        cls.protImport1 = cls.runImportMovies(cls.ds.getFile('qbeta/qbeta.mrc'),
                                              magnification=50000)
        cls.protImport2 = cls.runImportMovies(cls.ds.getFile('cct/cct_1.em'),
                                              magnification=61000)
    
    def _checkMicrographs(self, protocol, goldDimensions):
        self.assertIsNotNone(getattr(protocol, 'outputMicrographs', None),
                             "Output SetOfMicrographs were not created.")
        mic = protocol.outputMicrographs[1]
        x, y, _ = mic.getDim()
        dims = (x, y)
        msgError = "The dimensions must be %s and it is %s"
        self.assertEqual(goldDimensions, dims, msgError % (goldDimensions, dims))

    def _checkAlignment(self, movie, goldRange, goldRoi):
        alignment = movie.getAlignment()
        range = alignment.getRange()
        msgRange = "Alignment range must be %s %s and it is %s (%s)"
        self.assertEqual(goldRange, range,
                         msgRange % (goldRange, range, type(goldRange), type(range)))
        roi = alignment.getRoi()
        msgRoi = "Alignment ROI must be %s (%s) and it is %s (%s)"
        self.assertEqual(goldRoi, roi,
                         msgRoi % (goldRoi, roi, type(goldRoi), type(roi)))
    
    def test_qbeta(self):
        prot = self.newProtocol(XmippProtMovieCorr,
                                alignFrame0=3, alignFrameN=5,
                                cropOffsetX=10, cropOffsetY=10,
                                doSaveAveMic=False)
        prot.inputMovies.set(self.protImport1.outputMovies)
        self.launchProtocol(prot)
        
        self._checkAlignment(prot.outputMovies[1],
                             (3,5), [10, 10, 0, 0])
        
        protAverage = self.newProtocol(XmippProtMovieAverage,
                                       sumFrame0=3, sumFrameN=5,
                                       cropRegion=1)
        protAverage.inputMovies.set(prot.outputMovies)
        protAverage.setObjLabel('average w alignment info')
        self.launchProtocol(protAverage)
        
        self._checkMicrographs(protAverage, (4086,4086))
        protAverage2 = self.newProtocol(XmippProtMovieAverage,
                                        sumFrame0=3, sumFrameN=5,
                                       cropRegion=2)
        protAverage2.inputMovies.set(prot.outputMovies)
        protAverage2.setObjLabel('average w alignment')
        self.launchProtocol(protAverage2)

        self._checkMicrographs(protAverage2, (4096,4096))

    def test_cct(self):
        protAverage = self.newProtocol(XmippProtMovieAverage,
                                       cropRegion=2,
                                       sumFrame0=1, sumFrameN=7,
                                       cropOffsetX=10, cropOffsetY=10,
                                       cropDimX=1500, cropDimY=1500)
        protAverage.inputMovies.set(self.protImport2.outputMovies)
        protAverage.setObjLabel('average imported movies')
        self.launchProtocol(protAverage)

        self._checkMicrographs(protAverage, (1500,1500))

    def test_cct2(self):
        protAverage = self.newProtocol(XmippProtMovieAverage,
                                       cropRegion=1,
                                       sumFrame0=1, sumFrameN=7)
        protAverage.inputMovies.set(self.protImport2.outputMovies)
        protAverage.setObjLabel('average imported movies')
        self.launchProtocol(protAverage)

        self._checkMicrographs(protAverage, (4096,4096))


class TestEstimateGain(BaseTest):

    @classmethod
    def setUpClass(cls):
        setupTestProject(cls)
        ds = DataSet.getDataSet('movies')

        # Reduce input movie size to speed-up gain computation
        ih = ImageHandler()
        inputFn = ds.getFile('ribo/Falcon_2012_06_12-14_33_35_0_movie.mrcs')
        outputFn = cls.proj.getTmpPath(abspath(basename(inputFn)))

        frameImg = ih.createImage()
        xdim, ydim, zdim, ndim = ih.getDimensions(inputFn)
        n = max(zdim, ndim) / 2 # also half of the frames
        print "Scaling movie: %s -> %s" % (inputFn, outputFn)
        pwutils.cleanPath(outputFn)
        for i in range(1, n+1):
            frameImg.read((i, inputFn))
            frameImg.scale(xdim/2, ydim/2)
            frameImg.write((i, outputFn))

        args = cls.getArgs(outputFn)
        cls.protImport = cls.newProtocol(ProtImportMovies, **args)
        cls.launchProtocol(cls.protImport)

    @classmethod
    def getArgs(self, filesPath, pattern=''):
        return {'importFrom': ProtImportMovies.IMPORT_FROM_FILES,
                'filesPath': filesPath,
                'filesPattern': pattern,
                'amplitudConstrast': 0.1,
                'sphericalAberration': 2.,
                'voltage': 300,
                'samplingRate': 3.54 * 2
                }

    def test_estimate(self):
        protGain = self.newProtocol(XmippProtMovieGain,
                                    objLabel='estimate gain')
        protGain.inputMovies.set(self.protImport.outputMovies)
        protGain.useExistingGainImage.set(False)
        self.launchProtocol(protGain)


class TestExtractMovieParticles(BaseTest):
    @classmethod
    def setData(cls):
        cls.ds = DataSet.getDataSet('movies')
    
    @classmethod
    def runImportMovies(cls, pattern, **kwargs):
        """ Run an Import micrograph protocol. """
        # We have two options: passe the SamplingRate or
        # the ScannedPixelSize + microscope magnification
        params = {'samplingRate': 1.14,
                  'voltage': 300,
                  'sphericalAberration': 2.7,
                  'magnification': 50000,
                  'scannedPixelSize': None,
                  'filesPattern': pattern
                  }
        if 'samplingRate' not in kwargs:
            del params['samplingRate']
            params['samplingRateMode'] = 0
        else:
            params['samplingRateMode'] = 1
        
        params.update(kwargs)
        
        protImport = cls.newProtocol(ProtImportMovies, **params)
        cls.launchProtocol(protImport)
        return protImport
    
    @classmethod
    def setUpClass(cls):
        setupTestProject(cls)
        cls.setData()
        cls.protImport1 = cls.runImportMovies(cls.ds.getFile('qbeta/qbeta.mrc'),
                                              magnification=50000)
        cls.protImport2 = cls.runImportMovies(cls.ds.getFile('cct/cct_1.em'),
                                              magnification=61000)
    
    # def _checkMicrographs(self, protocol, goldDimensions):
    #     self.assertIsNotNone(getattr(protocol, 'outputMicrographs', None),
    #                          "Output SetOfMicrographs were not created.")
    #     mic = protocol.outputMicrographs[1]
    #     x, y, _ = mic.getDim()
    #     dims = (x, y)
    #     msgError = "The dimensions must be %s and it is %s"
    #     self.assertEqual(goldDimensions, dims,
    #                      msgError % (goldDimensions, dims))
    #
    def _checkAlignment(self, movie, goldRange, goldRoi):
        alignment = movie.getAlignment()
        range = alignment.getRange()
        msgRange = "Alignment range must be %s %s and it is %s (%s)"
        self.assertEqual(goldRange, range,
                         msgRange % (
                         goldRange, range, type(goldRange), type(range)))
        roi = alignment.getRoi()
        msgRoi = "Alignment ROI must be %s (%s) and it is %s (%s)"
        self.assertEqual(goldRoi, roi,
                         msgRoi % (goldRoi, roi, type(goldRoi), type(roi)))
    
    def test_qbeta(self):
        movAliProt = self.newProtocol(XmippProtMovieCorr,
                                alignFrame0=2, alignFrameN=6,
                                doSaveAveMic=True)
        movAliProt.inputMovies.set(self.protImport1.outputMovies)
        self.launchProtocol(movAliProt)
        
        self._checkAlignment(movAliProt.outputMovies[1],
                             (2, 6), [0, 0, 0, 0])
        
        importPick = self.newProtocol(ProtImportCoordinates,
                                 importFrom=ProtImportCoordinates.IMPORT_FROM_XMIPP,
                                 filesPath=self.ds.getFile('qbeta/'),
                                 filesPattern='*.pos', boxSize=320,
                                 invertX=False,
                                 invertY=False
                                 )
        importPick.inputMicrographs.set(movAliProt.outputMicrographs)
        importPick.setObjLabel('import coords from xmipp ')
        self.launchProtocol(importPick)

        protExtract = self.newProtocol(XmippProtExtractMovieParticles,
                                       boxSize=320,frame0=2,frameN=6,
                                       applyAlignment=True, doInvert=True)
        protExtract.inputMovies.set(movAliProt.outputMovies)
        protExtract.inputCoordinates.set(importPick.outputCoordinates)
        protExtract.setObjLabel('extract with alignment')
        self.launchProtocol(protExtract)
        
        self.assertIsNotNone(getattr(protExtract, 'outputParticles', None),
                             "Output SetOfMovieParticles were not created.")
        
        size = protExtract.outputParticles.getSize()
        self.assertEqual(size, 135, 'Number of particles must be 135 and its '
                                    '%d' % size)

    def test_cct(self):
        movAliProt = self.newProtocol(XmippProtMovieCorr,
                                      alignFrame0=2, alignFrameN=6,
                                      doSaveAveMic=True)
        movAliProt.inputMovies.set(self.protImport2.outputMovies)
        self.launchProtocol(movAliProt)

        self._checkAlignment(movAliProt.outputMovies[1],
                             (2, 6), [0, 0, 0, 0])

        importPick = self.newProtocol(ProtImportCoordinates,
                                      importFrom=ProtImportCoordinates.IMPORT_FROM_XMIPP,
                                      filesPath=self.ds.getFile('cct/'),
                                      filesPattern='*.pos', boxSize=320,
                                      invertX=False,
                                      invertY=False
                                      )
        importPick.inputMicrographs.set(movAliProt.outputMicrographs)
        importPick.setObjLabel('import coords from xmipp ')
        self.launchProtocol(importPick)

        protExtract = self.newProtocol(XmippProtExtractMovieParticles,
                                       boxSize=320, frame0=3, frameN=6,
                                       applyAlignment=False, doInvert=True)
        protExtract.inputMovies.set(movAliProt.outputMovies)
        protExtract.inputCoordinates.set(importPick.outputCoordinates)
        protExtract.setObjLabel('extract without alignment')
        self.launchProtocol(protExtract)

        self.assertIsNotNone(getattr(protExtract, 'outputParticles', None),
                             "Output SetOfMovieParticles were not created.")

        size = protExtract.outputParticles.getSize()
        self.assertEqual(size, 88, 'Number of particles must be 135 and its '
                                   '%d' % size)


class TestMaxShift(BaseTest):
    @classmethod
    def setData(cls):
        cls.ds = DataSet.getDataSet('movies')

    @classmethod
    def runImportMovies(cls, pattern, **kwargs):
        """ Run an Import movies protocol. """
        # We have two options: passe the SamplingRate or
        # the ScannedPixelSize + microscope magnification
        params = {'samplingRate': 1.14,
                  'voltage': 300,
                  'sphericalAberration': 2.7,
                  'magnification': 50000,
                  'scannedPixelSize': None,
                  'filesPattern': pattern
                  }
        if 'samplingRate' not in kwargs:
            del params['samplingRate']
            params['samplingRateMode'] = 0
        else:
            params['samplingRateMode'] = 1

        params.update(kwargs)

        protImport = cls.newProtocol(ProtImportMovies, **params)
        cls.launchProtocol(protImport)
        return protImport

    @classmethod
    def runAlignMovies(cls):  # do NOT save averaged mics
        protAlign = cls.newProtocol(XmippProtMovieCorr,
                                    alignFrame0=3, alignFrameN=5,
                                    cropOffsetX=10, cropOffsetY=16,
                                    objLabel='Movie alignment (NO save mic)',
                                    doSaveAveMic=False)
        protAlign.inputMovies.set(cls.protImport.outputMovies)
        cls.launchProtocol(protAlign)
        return protAlign.outputMovies

    @classmethod
    def runAlignMovMics(cls):  # do SAVE averaged mics
        protAlign = cls.newProtocol(XmippProtMovieCorr,
                                    alignFrame0=3, alignFrameN=5,
                                    cropOffsetX=10, cropOffsetY=16,
                                    objLabel='Movie alignment (SAVE mic)',
                                    doSaveAveMic=True)
        protAlign.inputMovies.set(cls.protImport.outputMovies)
        cls.launchProtocol(protAlign)
        return protAlign.outputMovies

    @classmethod
    def setUpClass(cls):
        setupTestProject(cls)
        cls.setData()
        fn = 'Falcon_2012_06_12-*0_movie.mrcs'
        cls.protImport = cls.runImportMovies(cls.ds.getFile(fn))
        cls.alignedMovies = cls.runAlignMovies()
        cls.alignedMovMics = cls.runAlignMovMics()

    def _checkMaxShiftFiltering(self, protocol, label, hasMic, rejOrPass=0):
        """ Check if outputSets are right.
              If hasMic=True then it's checked that micrographs are generated.
              If rejOrPass = 1: both movies should pass
                           =-1: both movies should be rejected
                           = 0: the first move should pass and the second not
        """

        def assertOutput(outputName, ids=[1, 2]):
            """ Check if outputName exist and if so, if it's right. (for each id)
            """
            if 'Micrographs' in outputName:
                # The alignment prot crops the micrographs
                inputDim = (1940, 1934, 1)
            else:
                inputDim = protocol.inputMovies.get().getDim()

            for itemId in ids:
                output = getattr(protocol, outputName, None)
                self.assertIsNotNone(output, "%s (accepted) were not created. "
                                             "Bad filtering in %s test."
                                     % (outputName, label))
                self.assertIsNotNone(output[itemId], "%s (accepted) were not "
                                            "created. Bad filtering in %s test."
                                     % (outputName, label))
                self.assertEqual(output[itemId].getDim(), inputDim,
                                 "The size of the movies/mics has change "
                                 "for %s test." % label)
                self.assertEqual(output[itemId].getSamplingRate(),
                             protocol.inputMovies.get().getSamplingRate(),
                             "The samplig rate of the movies has change for "
                             "%s test." % label)

        if rejOrPass == 1:
            #  Checking if only the accepted set is crated and
            #    its items have the good size and sampling rate
            assertOutput('outputMovies')
            if hasMic:
                assertOutput('outputMicrographs')

            #  Checking if the Movies/MicsDiscarded set are not created
            self.assertIsNone(getattr(protocol, 'outputMoviesDiscarded', None),
                              "outputMoviesDiscarded were created. "
                              "Bad filtering in %s test." % label)
            if hasMic:
                outMics = getattr(protocol, 'outputMicrographsDiscarded', None)
                self.assertIsNone(outMics, "outputMicrographsDiscarded were "
                                   "created. Bad filtering in %s test." % label)
        elif rejOrPass == -1:
            #  Checking if only the discarded set is crated and
            #    its items have the good size and sampling rate
            assertOutput('outputMoviesDiscarded')
            if hasMic:
                assertOutput('outputMicrographsDiscarded')
            #  Checking if the Movie (accepted) set is not created
            self.assertIsNone(getattr(protocol, 'outputMovies', None),
                              "outputMovies (accepted)t were created. "
                              "Bad filtering")
            if hasMic:
                self.assertIsNone(getattr(protocol, 'outputMicrographs', None),
                                  "outputMicrographs (accepted)t were created. "
                                  "Bad filtering")
        else:
            # Check if the passed and rejected movies corresponds to the goods.
            assertOutput('outputMovies', ids=[1])
            assertOutput('outputMoviesDiscarded', ids=[2])
            if hasMic:
                assertOutput('outputMicrographs', ids=[1])
                assertOutput('outputMicrographsDiscarded', ids=[2])
    
    def doFilter(self, inputMovies, rejType, label, mxFm=0.08, mxMo=0.09):
        """ Template for the movieMaxShift protocol.
        """
        protMaxShift = self.newProtocol(XmippProtMovieMaxShift,
                                        inputMovies=inputMovies,
                                        maxFrameShift=mxFm,
                                        maxMovieShift=mxMo,
                                        rejType=rejType,
                                         objLabel=label)
        self.launchProtocol(protMaxShift)
        return protMaxShift

    # ------- the Tests ---------------------------------------
    def testFilterFrame(self):
        """ This must discard the second movie for a Frame shift.
        """
        label = 'maxShift by Frame'
        rejType = XmippProtMovieMaxShift.REJ_FRAME

        protNoMic = self.doFilter(self.alignedMovies, rejType, label)
        self._checkMaxShiftFiltering(protNoMic, label, hasMic=0)

        protDoMic = self.doFilter(self.alignedMovMics, rejType, label)
        self._checkMaxShiftFiltering(protDoMic, label, hasMic=1)

    def testFilterMovie(self): 
        """ This must discard the second movie for a Global shift.
        """
        label = 'maxShift by Movie'
        rejType = XmippProtMovieMaxShift.REJ_MOVIE

        protNoMic = self.doFilter(self.alignedMovies, rejType, label)
        self._checkMaxShiftFiltering(protNoMic, label, hasMic=False)

        protDoMic = self.doFilter(self.alignedMovMics, rejType, label)
        self._checkMaxShiftFiltering(protDoMic, label, hasMic=True)

    def testFilterAnd(self): 
        """ This must discard the second movie for AND.
        """
        label = 'maxShift AND'
        rejType = XmippProtMovieMaxShift.REJ_AND

        protNoMic = self.doFilter(self.alignedMovies, rejType, label)
        self._checkMaxShiftFiltering(protNoMic, label, hasMic=False)

        protDoMic = self.doFilter(self.alignedMovMics, rejType, label)
        self._checkMaxShiftFiltering(protDoMic, label, hasMic=True)

    def testFilterOrFrame(self): 
        """ This must discard the second movie for OR (Frame).
        """
        label = 'maxShift OR (by frame)'
        rejType = XmippProtMovieMaxShift.REJ_OR

        protNoMic = self.doFilter(self.alignedMovies, rejType, label, mxMo=1)
        self._checkMaxShiftFiltering(protNoMic, label, hasMic=False)

        protDoMic = self.doFilter(self.alignedMovMics, rejType, label)
        self._checkMaxShiftFiltering(protDoMic, label, hasMic=True)

    def testFilterOrMovie(self): 
        """ This must discard the second movie for OR (Movie).
        """
        label = 'maxShift OR (by movie)'
        rejType = XmippProtMovieMaxShift.REJ_OR

        protNoMic = self.doFilter(self.alignedMovies, rejType, label, mxFm=1)
        self._checkMaxShiftFiltering(protNoMic, label, hasMic=False)

        protDoMic = self.doFilter(self.alignedMovMics, rejType, label)
        self._checkMaxShiftFiltering(protDoMic, label, hasMic=True)

    def testFilterOrBoth(self): 
        """ This must discard the second movie for OR (both).
        """
        label = 'maxShift OR (by both)'
        rejType = XmippProtMovieMaxShift.REJ_OR

        protNoMic = self.doFilter(self.alignedMovies, rejType, label)
        self._checkMaxShiftFiltering(protNoMic, label, hasMic=False)

        protDoMic = self.doFilter(self.alignedMovMics, rejType, label)
        self._checkMaxShiftFiltering(protDoMic, label, hasMic=True)

    def testFilterRejectBoth(self):
        """ This must discard both movies.
        """
        label = 'maxShift REJECT both'
        rejType = XmippProtMovieMaxShift.REJ_OR

        protNoMic = self.doFilter(self.alignedMovies, rejType, label, mxMo=0.01)
        self._checkMaxShiftFiltering(protNoMic, label, hasMic=False, rejOrPass=-1)

        protDoMic = self.doFilter(self.alignedMovMics, rejType, label, mxMo=0.01)
        self._checkMaxShiftFiltering(protDoMic, label, hasMic=True, rejOrPass=-1)

    def testFilterAcceptBoth(self):
        """ This must accept both movies.
        """
        label = 'maxShift ACCEPT both'
        rejType = XmippProtMovieMaxShift.REJ_AND

        protNoMic = self.doFilter(self.alignedMovies, rejType, label, mxMo=5)
        self._checkMaxShiftFiltering(protNoMic, label, hasMic=False, rejOrPass=1)

        protDoMic = self.doFilter(self.alignedMovMics, rejType, label, mxMo=5)
        self._checkMaxShiftFiltering(protDoMic, label, hasMic=True, rejOrPass=1)

