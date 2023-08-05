# **************************************************************************
# *
# * Authors:     J.M. De la Rosa Trevin (jmdelarosa@cnb.csic.es)
# *              Laura del Cano (ldelcano@cnb.csic.es)
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
"""
This module contains converter functions that will serve to:
1. Write from base classes to Xmipp specific files
2. Read from Xmipp files to base classes
"""

import os
from os.path import join, exists
from collections import OrderedDict
from itertools import izip
import numpy

from pyworkflow.em import Angles
from pyworkflow.utils import replaceBaseExt
from pyworkflow.em.data import *
from pyworkflow.em.convert import ImageHandler
import pyworkflow.em.metadata as md

import xmippLib
from xmipp3.base import XmippMdRow, getLabelPythonType, RowMetaData
from xmipp3.utils import iterMdRows


# This dictionary will be used to map
# between CTFModel properties and Xmipp labels
ACQUISITION_DICT = OrderedDict([
       ("_amplitudeContrast", xmippLib.MDL_CTF_Q0),
       ("_sphericalAberration", xmippLib.MDL_CTF_CS),
       ("_voltage", xmippLib.MDL_CTF_VOLTAGE)
       ])

COOR_DICT = OrderedDict([
             ("_x", xmippLib.MDL_XCOOR),
             ("_y", xmippLib.MDL_YCOOR)
             ])

COOR_EXTRA_LABELS = [
    # Additional autopicking-related metadata
    md.RLN_PARTICLE_AUTOPICK_FOM,
    md.RLN_PARTICLE_CLASS,
    md.RLN_ORIENT_PSI
    ]

CTF_DICT = OrderedDict([
       ("_defocusU", xmippLib.MDL_CTF_DEFOCUSU),
       ("_defocusV", xmippLib.MDL_CTF_DEFOCUSV),
       ("_defocusAngle", xmippLib.MDL_CTF_DEFOCUS_ANGLE),
       ("_resolution", xmippLib.MDL_CTF_CRIT_MAXFREQ),
       ("_fitQuality", xmippLib.MDL_CTF_CRIT_FITTINGSCORE)
       ])

# TODO: remove next dictionary when all
# cTFmodel has resolution and fitQuality
CTF_DICT_NORESOLUTION = OrderedDict([
        ("_defocusU", xmippLib.MDL_CTF_DEFOCUSU),
        ("_defocusV", xmippLib.MDL_CTF_DEFOCUSV),
        ("_defocusAngle", xmippLib.MDL_CTF_DEFOCUS_ANGLE)
        ])

CTF_PSD_DICT = OrderedDict([
       ("_psdFile", xmippLib.MDL_PSD),
       ("_xmipp_enhanced_psd", xmippLib.MDL_PSD_ENHANCED),
       ("_xmipp_ctfmodel_quadrant", xmippLib.MDL_IMAGE1),
       ("_xmipp_ctfmodel_halfplane", xmippLib.MDL_IMAGE1)
       ])

CTF_EXTRA_LABELS = [
    xmippLib.MDL_CTF_CA,
    xmippLib.MDL_CTF_ENERGY_LOSS,
    xmippLib.MDL_CTF_LENS_STABILITY,
    xmippLib.MDL_CTF_CONVERGENCE_CONE,
    xmippLib.MDL_CTF_LONGITUDINAL_DISPLACEMENT,
    xmippLib.MDL_CTF_TRANSVERSAL_DISPLACEMENT,
    xmippLib.MDL_CTF_K,
    xmippLib.MDL_CTF_BG_GAUSSIAN_K,
    xmippLib.MDL_CTF_BG_GAUSSIAN_SIGMAU,
    xmippLib.MDL_CTF_BG_GAUSSIAN_SIGMAV,
    xmippLib.MDL_CTF_BG_GAUSSIAN_CU,
    xmippLib.MDL_CTF_BG_GAUSSIAN_CV,
    xmippLib.MDL_CTF_BG_SQRT_K,
    xmippLib.MDL_CTF_BG_SQRT_U,
    xmippLib.MDL_CTF_BG_SQRT_V,
    xmippLib.MDL_CTF_BG_SQRT_ANGLE,
    xmippLib.MDL_CTF_BG_BASELINE,
    xmippLib.MDL_CTF_BG_GAUSSIAN2_K,
    xmippLib.MDL_CTF_BG_GAUSSIAN2_SIGMAU,
    xmippLib.MDL_CTF_BG_GAUSSIAN2_SIGMAV,
    xmippLib.MDL_CTF_BG_GAUSSIAN2_CU,
    xmippLib.MDL_CTF_BG_GAUSSIAN2_CV,
    xmippLib.MDL_CTF_BG_GAUSSIAN2_ANGLE,
    xmippLib.MDL_CTF_CRIT_FITTINGCORR13,
    xmippLib.MDL_CTF_CRIT_ICENESS,
    xmippLib.MDL_CTF_VPP_RADIUS,
    xmippLib.MDL_CTF_DOWNSAMPLE_PERFORMED,
    xmippLib.MDL_CTF_CRIT_PSDVARIANCE,
    xmippLib.MDL_CTF_CRIT_PSDPCA1VARIANCE,
    xmippLib.MDL_CTF_CRIT_PSDPCARUNSTEST,
    xmippLib.MDL_CTF_CRIT_FIRSTZEROAVG,
    xmippLib.MDL_CTF_CRIT_DAMPING,
    xmippLib.MDL_CTF_CRIT_FIRSTZERORATIO,
    xmippLib.MDL_CTF_CRIT_PSDCORRELATION90,
    xmippLib.MDL_CTF_CRIT_PSDRADIALINTEGRAL,
    xmippLib.MDL_CTF_CRIT_NORMALITY,
    # In xmipp the ctf also contains acquisition information
    xmippLib.MDL_CTF_Q0,
    xmippLib.MDL_CTF_CS,
    xmippLib.MDL_CTF_VOLTAGE,
    xmippLib.MDL_CTF_SAMPLING_RATE
    ]

# TODO: remove next dictionary when all
# cTFmodel has resolution and fitquality
CTF_EXTRA_LABELS_PLUS_RESOLUTION = [
    xmippLib.MDL_CTF_CA,
    xmippLib.MDL_CTF_ENERGY_LOSS,
    xmippLib.MDL_CTF_LENS_STABILITY,
    xmippLib.MDL_CTF_CONVERGENCE_CONE,
    xmippLib.MDL_CTF_LONGITUDINAL_DISPLACEMENT,
    xmippLib.MDL_CTF_TRANSVERSAL_DISPLACEMENT,
    xmippLib.MDL_CTF_K,
    xmippLib.MDL_CTF_BG_GAUSSIAN_K,
    xmippLib.MDL_CTF_BG_GAUSSIAN_SIGMAU,
    xmippLib.MDL_CTF_BG_GAUSSIAN_SIGMAV,
    xmippLib.MDL_CTF_BG_GAUSSIAN_CU,
    xmippLib.MDL_CTF_BG_GAUSSIAN_CV,
    xmippLib.MDL_CTF_BG_SQRT_K,
    xmippLib.MDL_CTF_BG_SQRT_U,
    xmippLib.MDL_CTF_BG_SQRT_V,
    xmippLib.MDL_CTF_BG_SQRT_ANGLE,
    xmippLib.MDL_CTF_BG_BASELINE,
    xmippLib.MDL_CTF_BG_GAUSSIAN2_K,
    xmippLib.MDL_CTF_BG_GAUSSIAN2_SIGMAU,
    xmippLib.MDL_CTF_BG_GAUSSIAN2_SIGMAV,
    xmippLib.MDL_CTF_BG_GAUSSIAN2_CU,
    xmippLib.MDL_CTF_BG_GAUSSIAN2_CV,
    xmippLib.MDL_CTF_BG_GAUSSIAN2_ANGLE,
    xmippLib.MDL_CTF_CRIT_MAXFREQ,  # ###
    xmippLib.MDL_CTF_CRIT_FITTINGSCORE,  # ###
    xmippLib.MDL_CTF_CRIT_FITTINGCORR13,
    xmippLib.MDL_CTF_CRIT_ICENESS,
    xmippLib.MDL_CTF_DOWNSAMPLE_PERFORMED,
    xmippLib.MDL_CTF_CRIT_PSDVARIANCE,
    xmippLib.MDL_CTF_CRIT_PSDPCA1VARIANCE,
    xmippLib.MDL_CTF_CRIT_PSDPCARUNSTEST,
    xmippLib.MDL_CTF_CRIT_FIRSTZEROAVG,
    xmippLib.MDL_CTF_CRIT_DAMPING,
    xmippLib.MDL_CTF_CRIT_FIRSTZERORATIO,
    xmippLib.MDL_CTF_CRIT_PSDCORRELATION90,
    xmippLib.MDL_CTF_CRIT_PSDRADIALINTEGRAL,
    xmippLib.MDL_CTF_CRIT_NORMALITY,
    # In xmipp the ctf also contains acquisition information
    xmippLib.MDL_CTF_Q0,
    xmippLib.MDL_CTF_CS,
    xmippLib.MDL_CTF_VOLTAGE,
    xmippLib.MDL_CTF_SAMPLING_RATE,
    xmippLib.MDL_CTF_VPP_RADIUS,
    ]

# Some extra labels to take into account the zscore
IMAGE_EXTRA_LABELS = [
    xmippLib.MDL_ZSCORE,
    xmippLib.MDL_ZSCORE_HISTOGRAM,
    xmippLib.MDL_ZSCORE_RESMEAN,
    xmippLib.MDL_ZSCORE_RESVAR,
    xmippLib.MDL_ZSCORE_RESCOV,
    xmippLib.MDL_ZSCORE_SHAPE1,
    xmippLib.MDL_ZSCORE_SHAPE2,
    xmippLib.MDL_ZSCORE_SNR1,
    xmippLib.MDL_ZSCORE_SNR2,
    xmippLib.MDL_CUMULATIVE_SSNR,
    xmippLib.MDL_PARTICLE_ID,
    xmippLib.MDL_FRAME_ID,
    xmippLib.MDL_SCORE_BY_VAR,
    xmippLib.MDL_SCORE_BY_GINI,
    xmippLib.MDL_ZSCORE_DEEPLEARNING1
    ]

ANGLES_DICT = OrderedDict([
       ("_angleY", xmippLib.MDL_ANGLE_Y),
       ("_angleY2", xmippLib.MDL_ANGLE_Y2),
       ("_angleTilt", xmippLib.MDL_ANGLE_TILT)
       ])

ALIGNMENT_DICT = OrderedDict([
       ("_xmipp_shiftX", xmippLib.MDL_SHIFT_X),
       ("_xmipp_shiftY", xmippLib.MDL_SHIFT_Y),
       ("_xmipp_shiftZ", xmippLib.MDL_SHIFT_Z),
       ("_xmipp_flip", xmippLib.MDL_FLIP),
       ("_xmipp_anglePsi", xmippLib.MDL_ANGLE_PSI),
       ("_xmipp_angleRot", xmippLib.MDL_ANGLE_ROT),
       ("_xmipp_angleTilt", xmippLib.MDL_ANGLE_TILT),
       ])


def objectToRow(obj, row, attrDict, extraLabels=[]):
    """ This function will convert an EMObject into a XmippMdRow.
    Params:
        obj: the EMObject instance (input)
        row: the XmippMdRow instance (output)
        attrDict: dictionary with the map between obj attributes(keys) and
            row MDLabels in Xmipp (values).
        extraLabels: a list with extra labels that could be included
            as _xmipp_labelName
    """
    if obj.isEnabled():
        enabled = 1
    else:
        enabled = -1
    row.setValue(xmippLib.MDL_ENABLED, enabled)

    for attr, label in attrDict.iteritems():
        if hasattr(obj, attr):
            valueType = getLabelPythonType(label)
            value = getattr(obj, attr).get()
            try:
                row.setValue(label, valueType(value))
            except Exception as e:
                print e
                print "Problems found converting metadata: "
                print "Label id = %s" % label
                print "Attribute = %s" % attr
                print "Value = %s" % value
                print "Value type = %s" % valueType
                raise e
            row.setValue(label, valueType(getattr(obj, attr).get()))
            
    attrLabels = attrDict.values()

    for label in extraLabels:
        attrName = '_xmipp_%s' % xmippLib.label2Str(label)
        if label not in attrLabels and hasattr(obj, attrName):
            value = obj.getAttributeValue(attrName)
            row.setValue(label, value)


def rowToObject(row, obj, attrDict, extraLabels=[]):
    """ This function will convert from a XmippMdRow to an EMObject.
    Params:
        row: the XmippMdRow instance (input)
        obj: the EMObject instance (output)
        attrDict: dictionary with the map between obj attributes(keys) and
            row MDLabels in Xmipp (values).
        extraLabels: a list with extra labels that could be included
            as _xmipp_labelName
    """
    obj.setEnabled(row.getValue(xmippLib.MDL_ENABLED, 1) > 0)

    for attr, label in attrDict.iteritems():
        value = row.getValue(label)
        if not hasattr(obj, attr):
            setattr(obj, attr, ObjectWrap(value))
        else:
            getattr(obj, attr).set(value)

    attrLabels = attrDict.values()

    for label in extraLabels:
        if label not in attrLabels and row.hasLabel(label):
            labelStr = xmippLib.label2Str(label)
            setattr(obj, '_xmipp_%s' % labelStr, row.getValueAsObject(label))

def setXmippAttributes(obj, objRow, *labels):
    """ Set an attribute to obj from a label that is not
    basic ones. The new attribute will be named _xmipp_LabelName
    and the datatype will be set correctly.
    """
    for label in labels:
        value = objRow.getValueAsObject(label)
        # To avoid empty values

        if objRow.containsLabel(label):
            setXmippAttribute(obj, label, value)

def setXmippAttribute(obj, label, value):
    """ Sets an attribute of an object prefixing it with xmipp"""
    setattr(obj, prefixAttribute(xmippLib.label2Str(label)), value)

def prefixAttribute(attribute):
    return '_xmipp_%s' % attribute

def rowFromMd(md, objId):
    row = XmippMdRow()
    row.readFromMd(md, objId)
    return row


def _containsAll(row, labels):
    """ Check if the labels (values) in labelsDict
    are present in the row.
    """
    values = labels.values() if isinstance(labels, dict) else labels
    return all(row.containsLabel(l) for l in values)


def _containsAny(row, labels):
    """ Check if the labels (values) in labelsDict
    are present in the row.
    """
    values = labels.values() if isinstance(labels, dict) else labels
    return any(row.containsLabel(l) for l in values)


def _rowToObjectFunc(obj):
    """ From a given object, return the function rowTo{OBJECT_CLASS_NAME}. """
    return globals()['rowTo' + obj.getClassName()]


def _readSetFunc(obj):
    """ From a given object, return the function read{OBJECT_CLASS_NAME}. """
    return globals()['read' + obj.getClassName()]


def locationToXmipp(index, filename):
    """ Convert an index and filename location
    to a string with @ as expected in Xmipp.
    """
    return ImageHandler.locationToXmipp((index, filename))


def fixVolumeFileName(image):
    """ This method will add :mrc to .mrc volumes
    because for mrc format is not possible to distinguish
    between 3D volumes and 2D stacks.
    """
    return ImageHandler.fixXmippVolumeFileName(image)


def getMovieFileName(movie):
    """ Add the :mrcs or :ems extensions to movie files to be
    recognized by Xmipp as proper stack files.
    """
    fn = movie.getFileName()
    if fn.endswith('.mrc'):
        fn += ':mrcs'
    elif fn.endswith('.em'):
        fn += ':ems'

    return fn


def getImageLocation(image):
    return ImageHandler.locationToXmipp(image)


def xmippToLocation(xmippFilename):
    """ Return a location (index, filename) given
    a Xmipp filename with the index@filename structure. """
    if '@' in xmippFilename:
        return xmippLib.FileName(xmippFilename).decompose()
    else:
        return NO_INDEX, str(xmippFilename)


def setObjId(obj, mdRow, label=xmippLib.MDL_ITEM_ID):
    if mdRow.containsLabel(label):
        obj.setObjId(mdRow.getValue(label))
    else:
        obj.setObjId(None)


def setRowId(mdRow, obj, label=xmippLib.MDL_ITEM_ID):
    mdRow.setValue(label, long(obj.getObjId()))


def micrographToCTFParam(mic, ctfparam):
    """ This function is used to convert a Micrograph object
    to the .ctfparam metadata needed by some Xmipp programs.
    If the micrograph already comes from xmipp, the ctfparam
    will be returned, if not, the new file.
    """
    ctf = mic.getCTF()

    if hasattr(ctf, '_xmippMd'):
        return ctf._xmippMd.get()

    md = xmippLib.MetaData()
    md.setColumnFormat(False)
    row = XmippMdRow()
    ctfModelToRow(ctf, row)
    acquisitionToRow(mic.getAcquisition(), row)
    row.writeToMd(md, md.addObject())
    md.write(ctfparam)
    return ctfparam


def imageToRow(img, imgRow, imgLabel, **kwargs):
    # Provide a hook to be used if something is needed to be
    # done for special cases before converting image to row
    preprocessImageRow = kwargs.get('preprocessImageRow', None)
    if preprocessImageRow:
        preprocessImageRow(img, imgRow)

    setRowId(imgRow, img)  # Set the id in the metadata as MDL_ITEM_ID
    index, filename = img.getLocation()
    fn = locationToXmipp(index, filename)
    imgRow.setValue(imgLabel, fn)

    if kwargs.get('writeCtf', True) and img.hasCTF():
        ctfModelToRow(img.getCTF(), imgRow)

    # alignment is mandatory at this point, it shoud be check
    # and detected defaults if not passed at readSetOf.. level
    alignType = kwargs.get('alignType')

    if alignType != ALIGN_NONE:
        alignmentToRow(img.getTransform(), imgRow, alignType)

    if kwargs.get('writeAcquisition', True) and img.hasAcquisition():
        acquisitionToRow(img.getAcquisition(), imgRow)

    # Write all extra labels to the row
    objectToRow(img, imgRow, {}, extraLabels=IMAGE_EXTRA_LABELS)

    # Provide a hook to be used if something is needed to be
    # done for special cases before converting image to row
    postprocessImageRow = kwargs.get('postprocessImageRow', None)
    if postprocessImageRow:
        postprocessImageRow(img, imgRow)


def rowToImage(imgRow, imgLabel, imgClass, **kwargs):
    """ Create an Image from a row of a metadata. """
    img = imgClass()

    # Provide a hook to be used if something is needed to be
    # done for special cases before converting image to row
    preprocessImageRow = kwargs.get('preprocessImageRow', None)
    if preprocessImageRow:
        preprocessImageRow(img, imgRow)

    # Decompose Xmipp filename
    index, filename = xmippToLocation(imgRow.getValue(imgLabel))
    img.setLocation(index, filename)

    if imgRow.containsLabel(xmippLib.MDL_REF):
        img.setClassId(imgRow.getValue(xmippLib.MDL_REF))
    elif imgRow.containsLabel(xmippLib.MDL_REF3D):
        img.setClassId(imgRow.getValue(xmippLib.MDL_REF3D))

    if kwargs.get('readCtf', True):
        img.setCTF(rowToCtfModel(imgRow))

    # alignment is mandatory at this point, it shoud be check
    # and detected defaults if not passed at readSetOf.. level
    alignType = kwargs.get('alignType')

    if alignType != ALIGN_NONE:
        img.setTransform(rowToAlignment(imgRow, alignType))

    if kwargs.get('readAcquisition', True):
        img.setAcquisition(rowToAcquisition(imgRow))

    if kwargs.get('magnification', None):
        img.getAcquisition().setMagnification(kwargs.get("magnification"))

    setObjId(img, imgRow)
    # Read some extra labels
    rowToObject(imgRow, img, {},
                extraLabels=IMAGE_EXTRA_LABELS + kwargs.get('extraLabels', []))

    # Provide a hook to be used if something is needed to be
    # done for special cases before converting image to row
    postprocessImageRow = kwargs.get('postprocessImageRow', None)
    if postprocessImageRow:
        postprocessImageRow(img, imgRow)

    return img


def micrographToRow(mic, micRow, **kwargs):
    """ Set labels values from Micrograph mic to md row. """
    imageToRow(mic, micRow, imgLabel=xmippLib.MDL_MICROGRAPH, **kwargs)


def rowToMicrograph(micRow, **kwargs):
    """ Create a Micrograph object from a row of Xmipp metadata. """
    return rowToImage(micRow, xmippLib.MDL_MICROGRAPH, Micrograph, **kwargs)


def volumeToRow(vol, volRow, **kwargs):
    """ Set labels values from Micrograph mic to md row. """
    imageToRow(vol, volRow, imgLabel=xmippLib.MDL_IMAGE,
               writeAcquisition=False, **kwargs)


def rowToVolume(volRow, **kwargs):
    """ Create a Volume object from a row of Xmipp metadata. """
    return rowToImage(volRow, xmippLib.MDL_IMAGE, Volume, **kwargs)


def coordinateToRow(coord, coordRow, copyId=True):
    """ Set labels values from Coordinate coord to md row. """
    if copyId:
        setRowId(coordRow, coord)
    objectToRow(coord, coordRow, COOR_DICT, extraLabels=COOR_EXTRA_LABELS)
    if coord.getMicId():
        coordRow.setValue(xmippLib.MDL_MICROGRAPH, str(coord.getMicId()))


def rowToCoordinate(coordRow):
    """ Create a Coordinate from a row of a metadata. """
    # Check that all required labels are present in the row
    if _containsAll(coordRow, COOR_DICT):
        coord = Coordinate()
        rowToObject(coordRow, coord, COOR_DICT, extraLabels=COOR_EXTRA_LABELS)

        # Setup the micId if is integer value
        try:
            coord.setMicId(int(coordRow.getValue(xmippLib.MDL_MICROGRAPH_ID)))
        except Exception:
            pass
    else:
        coord = None

    return coord


def _rowToParticle(partRow, particleClass, **kwargs):
    """ Create a Particle from a row of a metadata. """
    # Since postprocessImage is intended to be after the object is
    # setup, we need to intercept it here and call it at the end
    postprocessImageRow = kwargs.get('postprocessImageRow', None)
    if postprocessImageRow:
        del kwargs['postprocessImageRow']

    img = rowToImage(partRow, xmippLib.MDL_IMAGE, particleClass, **kwargs)
    img.setCoordinate(rowToCoordinate(partRow))
    # copy micId if available
    # if not copy micrograph name if available
    try:
        if partRow.hasLabel(xmippLib.MDL_MICROGRAPH_ID):
            img.setMicId(partRow.getValue(xmippLib.MDL_MICROGRAPH_ID))
#        elif partRow.hasLabel(xmippLib.MDL_MICROGRAPH):
#            micName = partRow.getValue(xmippLib.MDL_MICROGRAPH)
#            img._micrograph = micName
#            print "setting micname as", micName
#            img.printAll()
#            print "getAttributes1", img._micrograph
#            print "getAttributes2", getattr(img,"_micrograph",'kk')
#        else:
#            print "WARNING: No micname"
    except Exception as e:
        print("Warning:", e.message)

    if postprocessImageRow:
        postprocessImageRow(img, partRow)

    return img


def rowToParticle(partRow, **kwargs):
    return _rowToParticle(partRow, Particle, **kwargs)


def rowToMovieParticle(partRow, **kwargs):
    return _rowToParticle(partRow, MovieParticle, **kwargs)


def particleToRow(part, partRow, **kwargs):
    """ Set labels values from Particle to md row. """
    imageToRow(part, partRow, xmippLib.MDL_IMAGE, **kwargs)
    coord = part.getCoordinate()
    if coord is not None:
        coordinateToRow(coord, partRow, copyId=False)
    if part.hasMicId():
        partRow.setValue(xmippLib.MDL_MICROGRAPH_ID, long(part.getMicId()))
        partRow.setValue(xmippLib.MDL_MICROGRAPH, str(part.getMicId()))


def rowToClass(classRow, classItem):
    """ Method base to create a class2D, class3D or classVol from
    a row of a metadata
    """
    setObjId(classItem, classRow, label=xmippLib.MDL_REF)

    if classRow.containsLabel(xmippLib.MDL_IMAGE):
        index, filename = xmippToLocation(classRow.getValue(xmippLib.MDL_IMAGE))
        img = classItem.REP_TYPE()
        # class id should be set previously from MDL_REF
#         classItem.setObjId(classRow.getObjId())
#         img.copyObjId(classItem)
        img.setLocation(index, filename)
        img.setSamplingRate(classItem.getSamplingRate())
        classItem.setRepresentative(img)

    return classItem


def class2DToRow(class2D, classRow):
    """ Set labels values from Class2D to md row. """

    if class2D.hasRepresentative():
        index, filename = class2D.getRepresentative().getLocation()
        fn = locationToXmipp(index, filename)
        classRow.setValue(xmippLib.MDL_IMAGE, fn)
    n = long(len(class2D))
    classRow.setValue(xmippLib.MDL_CLASS_COUNT, n)
    classRow.setValue(xmippLib.MDL_REF, int(class2D.getObjId()))
    classRow.setValue(xmippLib.MDL_ITEM_ID, long(class2D.getObjId()))


def ctfModelToRow(ctfModel, ctfRow):
    """ Set labels values from ctfModel to md row. """
    # TODO: compatibility check remove eventually
    if ctfModel.hasResolution():
        objectToRow(ctfModel, ctfRow, CTF_DICT,
                    extraLabels=CTF_EXTRA_LABELS)
        if ctfModel.hasPhaseShift():
            ctfRow.setValue(xmippLib.MDL_CTF_PHASE_SHIFT,
                            ctfModel.getPhaseShift())
    else:
        objectToRow(ctfModel, ctfRow, CTF_DICT_NORESOLUTION,
                    extraLabels=CTF_EXTRA_LABELS)


def defocusGroupSetToRow(defocusGroup, defocusGroupRow):
    """ Set labels values from ctfModel to md row. """
    objectToRow(defocusGroup, defocusGroupRow, CTF_DICT)


def setPsdFiles(ctfModel, ctfRow):
    """ Set the PSD files of CTF estimation related
    to this ctfModel. The values will be read from
    the ctfRow if present.
    """
    for attr, label in CTF_PSD_DICT.iteritems():
        if ctfRow.containsLabel(label):
            setattr(ctfModel, attr, String(ctfRow.getValue(label)))


def rowToCtfModel(ctfRow):
    """ Create a CTFModel from a row of a metadata. """
    # Check if the row has CTF values, this could be called from a xmipp
    # particles metadata
    if _containsAll(ctfRow, CTF_DICT_NORESOLUTION):

        # for compatibility reason ignore resolution and fitQuality
        # Instantiate Scipion CTF Model
        ctfModel = CTFModel()

        # Case for metadata coming with Xmipp resolution label
        # Populate Scipion CTF from metadata row (using mapping dictionary
        # plus extra labels
        if ctfRow.hasLabel(md.MDL_CTF_PHASE_SHIFT):
            ctfModel.setPhaseShift(ctfRow.getValue(md.MDL_CTF_PHASE_SHIFT, 0))
        if ctfRow.containsLabel(xmippLib.label2Str(xmippLib.MDL_CTF_CRIT_MAXFREQ)):
            rowToObject(ctfRow, ctfModel, CTF_DICT,
                        extraLabels=CTF_EXTRA_LABELS)
        else:
            rowToObject(ctfRow, ctfModel, CTF_DICT_NORESOLUTION,
                        extraLabels=CTF_EXTRA_LABELS_PLUS_RESOLUTION)

        # Standarize defocus values
        ctfModel.standardize()
        # Set psd file names
        setPsdFiles(ctfModel, ctfRow)
        # ctfModel.setPhaseShift(0.0)  # for consistency with ctfModel

    else:
        ctfModel = None

    return ctfModel


def acquisitionToRow(acquisition, ctfRow):
    """ Set labels values from acquisition to md row. """
    objectToRow(acquisition, ctfRow, ACQUISITION_DICT)


def rowToAcquisition(acquisitionRow):
    """ Create an acquisition from a row of a metadata. """
    if _containsAll(acquisitionRow, ACQUISITION_DICT):
        acquisition = Acquisition()
        rowToObject(acquisitionRow, acquisition, ACQUISITION_DICT)
    else:
        acquisition = None

    return acquisition


def readSetOfMicrographs(filename, micSet, **kwargs):
    readSetOfImages(filename, micSet, rowToMicrograph, **kwargs)


def writeSetOfMicrographs(micSet, filename, blockName='Micrographs', **kwargs):
    writeSetOfImages(micSet, filename, micrographToRow, blockName, **kwargs)


def readSetOfVolumes(filename, volSet, **kwargs):
    readSetOfImages(filename, volSet, rowToVolume, **kwargs)


def writeSetOfVolumes(volSet, filename, blockName='Volumes', **kwargs):
    writeSetOfImages(volSet, filename, volumeToRow, blockName, **kwargs)


def mdToCTFModel(md, mic):
    ctfRow = rowFromMd(md, md.firstObject())
    ctfObj = rowToCtfModel(ctfRow)
    setXmippAttributes(ctfObj, ctfRow,
                       xmippLib.MDL_CTF_CRIT_NONASTIGMATICVALIDITY,
                       xmippLib.MDL_CTF_CRIT_FIRSTMINIMUM_FIRSTZERO_DIFF_RATIO)
    ctfObj.setMicrograph(mic)

    return ctfObj


def readCTFModel(filename, mic):
    """ Read from Xmipp .ctfparam and create a CTFModel object. """
    md = xmippLib.MetaData(filename)
    return mdToCTFModel(md, mic)


def openMd(fn, state='Manual'):
    # We are going to write metadata directy to file to do it faster
    f = open(fn, 'w')
    ismanual = state == 'Manual'
    block = 'data_particles' if ismanual else 'data_particles_auto'
    s = """# XMIPP_STAR_1 *
#
data_header
loop_
 _pickingMicrographState
%s
%s
loop_
 _itemId
 _enabled
 _xcoor
 _ycoor
 _cost
 _micrographId
""" % (state, block)
    f.write(s)
    return f


def writeSetOfCoordinates(posDir, coordSet, ismanual=True, scale=1):
    state = 'Manual' if ismanual else 'Supervised'
    writeSetOfCoordinatesWithState(posDir, coordSet, state, scale)


def writeSetOfCoordinatesWithState(posDir, coordSet, state, scale=1):
    """ Write a pos file on metadata format for each micrograph
    on the coordSet.
    Params:
        posDir: the directory where the .pos files will be written.
        coordSet: the SetOfCoordinates that will be read.
    """
    boxSize = coordSet.getBoxSize() or 100

    # Create a dictionary with the pos filenames for each micrograph
    posDict = {}
    for mic in coordSet.iterMicrographs():
        micIndex, micFileName = mic.getLocation()
        micName = os.path.basename(micFileName)

        if micIndex != NO_INDEX:
            micName = '%06d_at_%s' % (micIndex, micName)

        posFn = join(posDir, replaceBaseExt(micName, "pos"))
        posDict[mic.getObjId()] = posFn

    f = None
    lastMicId = None
    c = 0

    for coord in coordSet.iterItems(orderBy='_micId'):
        micId = coord.getMicId()

        if micId != lastMicId:
            # we need to close previous opened file
            if f:
                f.close()
                c = 0
            f = openMd(posDict[micId], state)
            lastMicId = micId
        c += 1
        if scale != 1:
            x = coord.getX() * scale
            y = coord.getY() * scale
        else:
            x = coord.getX()
            y = coord.getY()
        f.write(" %06d   1   %d  %d  %d   %06d\n"
                % (coord.getObjId(), x, y, 1, micId))

    if f:
        f.close()

    # Write config.xmd metadata
    configFn = join(posDir, 'config.xmd')
    writeCoordsConfig(configFn, int(boxSize), state)

    return posDict.values()


def writeCoordsConfig(configFn, boxSize, state):
    """ Write the config.xmd file needed for Xmipp picker.
    Params:
        configFn: The filename were to store the configuration.
        boxSize: the box size in pixels for extraction.
        state: picker state
    """
    # Write config.xmd metadata
    print("writeCoordsConfig: state=", state)
    md = xmippLib.MetaData()
    # Write properties block
    objId = md.addObject()
    md.setValue(xmippLib.MDL_PICKING_PARTICLE_SIZE, int(boxSize), objId)
    md.setValue(xmippLib.MDL_PICKING_STATE, state, objId)
    md.write('properties@%s' % configFn)


def writeMicCoordinates(mic, coordList, outputFn, isManual=True,
                        getPosFunc=None):
    """ Write the pos file as expected by Xmipp with the coordinates
    of a given micrograph.
    Params:
        mic: input micrograph.
        coordList: list of (x, y) pairs of the mic coordinates.
        outputFn: output filename for the pos file .
        isManual: if the coordinates are 'Manual' or 'Supervised'
        getPosFunc: a function to get the positions from the coordinate,
            it can be useful for scaling the coordinates if needed.
    """
    if getPosFunc is None:
        getPosFunc = lambda coord: coord.getPosition()

    state = 'Manual' if isManual else 'Supervised'
    f = openMd(outputFn, state)

    for coord in coordList:
        x, y = getPosFunc(coord)
        f.write(" %06d   1   %d  %d  %d   %06d\n"
                % (coord.getObjId(), x, y, 1, mic.getObjId()))
    
    f.close()
    

def readSetOfCoordinates(outputDir, micSet, coordSet, readDiscarded=False):
    """ Read from Xmipp .pos files.
    Params:
        outputDir: the directory where the .pos files are.
            It is also expected a file named: config.xmd
            in this directory where the box size can be read.
        micSet: the SetOfMicrographs to associate the .pos, which
            name should be the same of the micrographs.
        coordSet: the SetOfCoordinates that will be populated.
        readDiscarded: read only the coordinates with the MDL_ENABLE set at -1
    """
    # Read the boxSize from the config.xmd metadata
    configfile = join(outputDir, 'config.xmd')
    if exists(configfile):
        md = xmippLib.MetaData('properties@' + join(outputDir, 'config.xmd'))
        boxSize = md.getValue(xmippLib.MDL_PICKING_PARTICLE_SIZE,
                              md.firstObject())
        coordSet.setBoxSize(boxSize)
    for mic in micSet:
        posFile = join(outputDir, replaceBaseExt(mic.getFileName(), 'pos'))
        readCoordinates(mic, posFile, coordSet, outputDir, readDiscarded)

    coordSet._xmippMd = String(outputDir)


def readCoordinates(mic, fileName, coordsSet, outputDir, readDiscarded=False):
        posMd = readPosCoordinates(fileName, readDiscarded)
        # TODO: CHECK IF THIS LABEL IS STILL NECESSARY
        posMd.addLabel(md.MDL_ITEM_ID)

        for objId in posMd:
            # When do an union of two metadatas of coordinates and one of
            # them doesn't has MDL_ENABLED, the default vaule to is 0,
            # and its not allowed value. Maybe we need to solve this in xmipp
            # code.
            if posMd.getValue(md.MDL_ENABLED, objId) == 0:
                posMd.setValue(md.MDL_ENABLED, 1, objId)

            coord = rowToCoordinate(rowFromMd(posMd, objId))
            coord.setMicrograph(mic)
            coord.setX(coord.getX())
            coord.setY(coord.getY())
            coordsSet.append(coord)
            posMd.setValue(md.MDL_ITEM_ID, long(coord.getObjId()), objId)


def readPosCoordinates(posFile, readDiscarded=False):
    """ Read the coordinates in .pos file and return corresponding metadata.
    There are two possible blocks with particles:
    particles: with manual/supervised particles
    particles_auto: with automatically picked particles.
    If posFile doesn't exist, the metadata will be empty
    readDiscarded: read only the coordinates in the particles_auto DB
                   with the MDL_ENABLE set at -1 and a positive cost
    """
    mData = md.MetaData()

    if exists(posFile):
        blocks = md.getBlocksInMetaDataFile(posFile)

        blocksToRead = ['particles_auto'] if readDiscarded \
                        else ['particles','particles_auto']

        for b in blocksToRead:
            if b in blocks:
                mdAux = md.MetaData('%(b)s@%(posFile)s' % locals())
                mData.unionAll(mdAux)
        if readDiscarded:
            for objId in mData:
                if mData.getValue(md.MDL_COST, objId)>0:
                    enabled=mData.getValue(md.MDL_ENABLED, objId)
                    mData.setValue(md.MDL_ENABLED, -1*enabled, objId)
        mData.removeDisabled()
    return mData


def readSetOfImages(filename, imgSet, rowToFunc, **kwargs):
    """read from Xmipp image metadata.
        filename: The metadata filename where the image are.
        imgSet: the SetOfParticles that will be populated.
        rowToFunc: this function will be used to convert the row to Object
    """
    imgMd = xmippLib.MetaData(filename)

    # By default remove disabled items from metadata
    # be careful if you need to preserve the original number of items
    if kwargs.get('removeDisabled', True):
        imgMd.removeDisabled()

    # If the type of alignment is not sent through the kwargs
    # try to deduced from the metadata labels
    if 'alignType' not in kwargs:
        imgRow = rowFromMd(imgMd, imgMd.firstObject())
        if _containsAny(imgRow, ALIGNMENT_DICT):
            if imgRow.containsLabel(xmippLib.MDL_ANGLE_TILT):
                kwargs['alignType'] = ALIGN_PROJ
            else:
                kwargs['alignType'] = ALIGN_2D
        else:
            kwargs['alignType'] = ALIGN_NONE

    if imgMd.size() > 0:
        for objId in imgMd:
            imgRow = rowFromMd(imgMd, objId)
            img = rowToFunc(imgRow, **kwargs)
            imgSet.append(img)

        imgSet.setHasCTF(img.hasCTF())
        imgSet.setAlignment(kwargs['alignType'])


def setOfImagesToMd(imgSet, md, imgToFunc, **kwargs):
    """ This function will fill Xmipp metadata from a SetOfMicrographs
    Params:
        imgSet: the set of images to be converted to metadata
        md: metadata to be filled
        rowFunc: this function can be used to setup the row before
            adding to metadata.
    """

    if 'alignType' not in kwargs:
        kwargs['alignType'] = imgSet.getAlignment()

    if 'where' in kwargs:
        where = kwargs['where']
        for img in imgSet.iterItems(where=where):
            objId = md.addObject()
            imgRow = XmippMdRow()
            imgToFunc(img, imgRow, **kwargs)
            imgRow.writeToMd(md, objId)
    else:
        for img in imgSet:
            objId = md.addObject()
            imgRow = XmippMdRow()
            imgToFunc(img, imgRow, **kwargs)
            imgRow.writeToMd(md, objId)


def readAnglesFromMicrographs(micFile, anglesSet):
    """ Read the angles from a micrographs Metadata.
    """
    micMd = xmippLib.MetaData(micFile)
#    micMd.removeDisabled()

    for objId in micMd:
        # TODO I have added the import from pyworkflow.em import Angles
        # because next line gave an error. I do not know if this
        # is the right Angle class
        angles = Angles()
        row = rowFromMd(micMd, objId)
        rowToObject(row, angles, ANGLES_DICT)
        angles.setObjId(micMd.getValue(xmippLib.MDL_ITEM_ID, objId))
        anglesSet.append(angles)


def writeSetOfImages(imgSet, filename, imgToFunc,
                     blockName='Images', **kwargs):
    """ This function will write a SetOfImages as a Xmipp metadata.
    Params:
        imgSet: the set of images to be written (particles,
        micrographs or volumes)
        filename: the filename where to write the metadata.
        rowFunc: this function can be used to setup the row before
            adding to metadata.
    """
    md = xmippLib.MetaData()

    setOfImagesToMd(imgSet, md, imgToFunc, **kwargs)
    md.write('%s@%s' % (blockName, filename))


def readSetOfParticles(filename, partSet, **kwargs):
    readSetOfImages(filename, partSet, rowToParticle, **kwargs)


def readSetOfMovieParticles(filename, partSet, **kwargs):
    readSetOfImages(filename, partSet, rowToMovieParticle, **kwargs)


def setOfParticlesToMd(imgSet, md, **kwargs):
    setOfImagesToMd(imgSet, md, particleToRow, **kwargs)


def setOfMicrographsToMd(imgSet, md, **kwargs):
    setOfImagesToMd(imgSet, md, micrographToRow, **kwargs)


def writeSetOfParticles(imgSet, filename, blockName='Particles', **kwargs):
    writeSetOfImages(imgSet, filename, particleToRow, blockName, **kwargs)


def writeCTFModel(ctfModel, ctfFile):
    """ Given a CTFModel object write as Xmipp ctfparam
    """
    md = xmippLib.MetaData()

    objId = md.addObject()
    ctfRow = XmippMdRow()
    ctfModelToRow(ctfModel, ctfRow)
    ctfRow.writeToMd(md, objId)

    md.setColumnFormat(False)
    md.write(ctfFile)


def writeSetOfCTFs(ctfSet, mdCTF):
    """ Write a ctfSet on metadata format.
    Params:
        ctfSet: the SetOfCTF that will be read.
        mdCTF: The file where metadata should be written.
    """
    md = xmippLib.MetaData()

    for ctfModel in ctfSet:
        objId = md.addObject()
        ctfRow = XmippMdRow()
        ctfRow.setValue(xmippLib.MDL_MICROGRAPH, ctfModel.getMicFile())
        if ctfModel.getPsdFile():
            ctfRow.setValue(xmippLib.MDL_PSD, ctfModel.getPsdFile())
        ctfModelToRow(ctfModel, ctfRow)
        ctfRow.writeToMd(md, objId)

    md.write(mdCTF)
    ctfSet._xmippMd = String(mdCTF)


def writeSetOfDefocusGroups(defocusGroupSet, fnDefocusGroup):  # also metadata
    """ Write a defocuGroupSet on metadata format.
    Params:
        defocusGroupSet: the SetOfDefocus that will be read.
        fnDefocusGroup: The file where defocusGroup should be written.
    """
    md = xmippLib.MetaData()

    for defocusGroup in defocusGroupSet:
        objId = md.addObject()
        defocusGroupRow = XmippMdRow()
        defocusGroupSetToRow(defocusGroup, defocusGroupRow)
        defocusGroupRow.setValue(xmippLib.MDL_CTF_GROUP, defocusGroup.getObjId())
        defocusGroupRow.setValue(xmippLib.MDL_MIN, defocusGroup.getDefocusMin())
        defocusGroupRow.setValue(xmippLib.MDL_MAX, defocusGroup.getDefocusMax())
        defocusGroupRow.setValue(xmippLib.MDL_AVG, defocusGroup.getDefocusAvg())
        defocusGroupRow.writeToMd(md, objId)

    md.write(fnDefocusGroup)
    defocusGroupSet._xmippMd = String(fnDefocusGroup)


def writeSetOfClasses2D(classes2DSet, filename,
                        classesBlock='classes', writeParticles=True):
    """ This function will write a SetOfClasses2D as Xmipp metadata.
    Params:
        classes2DSet: the SetOfClasses2D instance.
        filename: the filename where to write the metadata.
    """
    classFn = '%s@%s' % (classesBlock, filename)
    classMd = xmippLib.MetaData()
    classMd.write(classFn)  # Empty write to ensure the classes is the first
    # block

    classRow = XmippMdRow()
    for class2D in classes2DSet:
        class2DToRow(class2D, classRow)
        classRow.writeToMd(classMd, classMd.addObject())
        if writeParticles:
            ref = class2D.getObjId()
            imagesFn = 'class%06d_images@%s' % (ref, filename)
            imagesMd = xmippLib.MetaData()
            imgRow = XmippMdRow()
            if class2D.getSize() > 0:
                for img in class2D:
                    particleToRow(img, imgRow)
                    imgRow.writeToMd(imagesMd, imagesMd.addObject())
            imagesMd.write(imagesFn, xmippLib.MD_APPEND)

    # Empty write to ensure the classes is the first block
    classMd.write(classFn, xmippLib.MD_APPEND)


def writeSetOfMicrographsPairs(uSet, tSet, filename):
    """ This function will write a MicrographsTiltPair as Xmipp metadata.
    Params:
        uSet: the untilted set of micrographs to be written
        tSet: the tilted set of micrographs to be written
        filename: the filename where to write the metadata.
    """
    md = xmippLib.MetaData()

    for micU, micT in izip(uSet, tSet):
        objId = md.addObject()
        pairRow = XmippMdRow()
        pairRow.setValue(xmippLib.MDL_ITEM_ID, long(micU.getObjId()))
        pairRow.setValue(xmippLib.MDL_MICROGRAPH, micU.getFileName())
        pairRow.setValue(xmippLib.MDL_MICROGRAPH_TILTED, micT.getFileName())
        pairRow.writeToMd(md, objId)

    md.write(filename)


def __readSetOfClasses(classBaseSet, readSetFunc,
                       classesSet, filename, classesBlock='classes', **kwargs):
    """ Read a set of classes from an Xmipp metadata with the given
    convention of a block for classes and another block for each set of
    images assigned to each class.
    Params:
        classesSet: the SetOfClasses object that will be populated.
        filename: the file path where to read the Xmipp metadata.
        classesBlock (by default 'classes'):
            the block name of the classes group in the metadata.
    """
    blocks = xmippLib.getBlocksInMetaDataFile(filename)

    classesMd = xmippLib.MetaData('%s@%s' % (classesBlock, filename))

    # Provide a hook to be used if something is needed to be
    # done for special cases before converting row to class
    preprocessClass = kwargs.get('preprocessClass', None)
    postprocessClass = kwargs.get('postprocessClass', None)

    for objId in classesMd:
        classItem = classesSet.ITEM_TYPE()
        classRow = rowFromMd(classesMd, objId)
        # class id should be set in rowToClass function using MDL_REF
        classItem = rowToClass(classRow, classItem)

        classBaseSet.copyInfo(classItem, classesSet.getImages())

        if preprocessClass:
            preprocessClass(classItem, classRow)

        classesSet.append(classItem)

        ref = classItem.getObjId()
        b = 'class%06d_images' % ref

        if b in blocks:
            readSetFunc('%s@%s' % (b, filename), classItem, **kwargs)

        if postprocessClass:
            postprocessClass(classItem, classRow)

        # Update with new properties of classItem such as _size
        classesSet.update(classItem)


def readSetOfClasses(classesSet, filename, classesBlock='classes', **kwargs):
    __readSetOfClasses(SetOfParticles, readSetOfParticles,
                       classesSet, filename, classesBlock, **kwargs)


def readSetOfClasses2D(classes2DSet, filename,
                       classesBlock='classes', **kwargs):
    """ Just a wrapper to readSetOfClasses. """
    readSetOfClasses(classes2DSet, filename, classesBlock, **kwargs)


def readSetOfClasses3D(classes3DSet, filename,
                       classesBlock='classes', **kwargs):
    """ Just a wrapper to readSetOfClasses. """
    readSetOfClasses(classes3DSet, filename, classesBlock, **kwargs)


def writeSetOfClassesVol(classesVolSet, filename, classesBlock='classes'):
    """ This function will write a SetOfClassesVol as Xmipp metadata.
    Params:
        classesVolSet: the SetOfClassesVol instance.
        filename: the filename where to write the metadata.
    """
    classFn = '%s@%s' % (classesBlock, filename)
    classMd = xmippLib.MetaData()
    classMd.write(classFn)  # Empty write to ensure the classes is the first
    # block
    # FIXME: review implementation of this function since there are syntax
    # errors
    classRow = XmippMdRow()
    for classVol in classesVolSet:
        classVolToRow(classVol, classRow)
        classRow.writeToMd(classMd, classMd.addObject())
        ref = class3D.getObjId()
        imagesFn = 'class%06d_images@%s' % (ref, filename)
        imagesMd = xmippLib.MetaData()
        imgRow = XmippMdRow()

        for vol in classVol:
            volumeToRow(vol, imgRow)
            imgRow.writeToMd(imagesMd, imagesMd.addObject())
        imagesMd.write(imagesFn, xmippLib.MD_APPEND)

    # Empty write to ensure the classes is the first block
    classMd.write(classFn, xmippLib.MD_APPEND)


def readSetOfClassesVol(classesVolSet, filename,
                        classesBlock='classes', **kwargs):
    """read from Xmipp image metadata.
        fnImages: The metadata filename where the particles properties are.
        imgSet: the SetOfParticles that will be populated.
        hasCtf: is True if the ctf information exists.
    """
    __readSetOfClasses(SetOfVolumes, readSetOfVolumes,
                       classesVolSet, filename, classesBlock, **kwargs)

def writeSetOfMovies(moviesSet, filename, moviesBlock='movies'):
    """ This function will write a SetOfMovies as Xmipp metadata.
    Params:
        moviesSet: the SetOfMovies instance.
        filename: the filename where to write the metadata.
    """

    for movie in moviesSet:

        ref = movie.getObjId()
        micrographsFn = 'movie%06d_micrographs@%s' % (ref, filename)
        micrographsMd = xmippLib.MetaData()
        micRow = XmippMdRow()

        for mic in movie:
            micrographToRow(mic, micRow)
            micRow.writeToMd(micrographsMd, micrographsMd.addObject())
        micrographsMd.write(micrographsFn, xmippLib.MD_APPEND)

def geometryFromMatrix(matrix, inverseTransform):
    from pyworkflow.em.convert.transformations import  \
        translation_from_matrix, euler_from_matrix
    if inverseTransform:
        matrix = numpy.linalg.inv(matrix)
        shifts = -translation_from_matrix(matrix)
    else:
        shifts = translation_from_matrix(matrix)
    angles = -numpy.rad2deg(euler_from_matrix(matrix, axes='szyz'))
    return shifts, angles


def matrixFromGeometry(shifts, angles, inverseTransform):
    """ Create the transformation matrix from a given
    2D shifts in X and Y...and the 3 euler angles.
    """
    from pyworkflow.em.convert.transformations import  euler_matrix
    radAngles = -numpy.deg2rad(angles)

    M = euler_matrix(radAngles[0], radAngles[1], radAngles[2], 'szyz')
    if inverseTransform:
        M[:3, 3] = -shifts[:3]
        M = numpy.linalg.inv(M)
    else:
        M[:3, 3] = shifts[:3]

    return M


def rowToAlignment(alignmentRow, alignType):
    """
    is2D == True-> matrix is 2D (2D images alignment)
            otherwise matrix is 3D (3D volume alignment or projection)
    invTransform == True  -> for xmipp implies projection
        """
    is2D = alignType == ALIGN_2D
    inverseTransform = alignType == ALIGN_PROJ

    if _containsAny(alignmentRow, ALIGNMENT_DICT):
        alignment = Transform()
        angles = numpy.zeros(3)
        shifts = numpy.zeros(3)
        flip = alignmentRow.getValue(xmippLib.MDL_FLIP)

        shifts[0] = alignmentRow.getValue(xmippLib.MDL_SHIFT_X, 0.)
        shifts[1] = alignmentRow.getValue(xmippLib.MDL_SHIFT_Y, 0.)
        if not is2D:
            angles[0] = alignmentRow.getValue(xmippLib.MDL_ANGLE_ROT, 0.)
            angles[1] = alignmentRow.getValue(xmippLib.MDL_ANGLE_TILT, 0.)
            shifts[2] = alignmentRow.getValue(xmippLib.MDL_SHIFT_Z, 0.)
            angles[2] = alignmentRow.getValue(xmippLib.MDL_ANGLE_PSI, 0.)
            if flip:
                angles[1] = angles[1]+180  # tilt + 180
                angles[2] = - angles[2]    # - psi, COSS: this is mirroring X
                shifts[0] = -shifts[0]     # -x
        else:
            psi = alignmentRow.getValue(xmippLib.MDL_ANGLE_PSI, 0.)
            rot = alignmentRow.getValue(xmippLib.MDL_ANGLE_ROT, 0.)
            if rot != 0. and psi != 0:
                print "HORROR rot and psi are different from zero in 2D case"
            angles[0] = \
                alignmentRow.getValue(xmippLib.MDL_ANGLE_PSI, 0.)\
                + alignmentRow.getValue(xmippLib.MDL_ANGLE_ROT, 0.)

        matrix = matrixFromGeometry(shifts, angles, inverseTransform)

        if flip:
            if alignType == ALIGN_2D:
                matrix[0, :2] *= -1.  # invert only the first two columns
                # keep x
                matrix[2, 2] = -1.  # set 3D rot
            elif alignType == ALIGN_3D:
                matrix[0, :3] *= -1.  # now, invert first line excluding x
                matrix[3, 3] *= -1.
            elif alignType == ALIGN_PROJ:
                pass

        alignment.setMatrix(matrix)

        # FIXME: now are also storing the alignment parameters since
        # the conversions to the Transform matrix have not been extensively
        # tested.
        # After this, we should only keep the matrix
        # for paramName, label in ALIGNMENT_DICT.iteritems():
        #    if alignmentRow.hasLabel(label):
        #        setattr(alignment, paramName,
        #                alignmentRow.getValueAsObject(label))
    else:
        alignment = None

    return alignment


def alignmentToRow(alignment, alignmentRow, alignType):
    """
    is2D == True-> matrix is 2D (2D images alignment)
            otherwise matrix is 3D (3D volume alignment or projection)
    invTransform == True  -> for xmipp implies projection
                          -> for xmipp implies alignment
    """
    if alignment is None:
        return

    is2D = alignType == ALIGN_2D
    inverseTransform = alignType == ALIGN_PROJ
    # only flip is meaninfull if 2D case
    # in that case the 2x2 determinant is negative
    flip = False
    matrix = alignment.getMatrix()
    if alignType == ALIGN_2D:
        # get 2x2 matrix and check if negative
        flip = bool(numpy.linalg.det(matrix[0:2, 0:2]) < 0)
        if flip:
            matrix[0, :2] *= -1.  # invert only the first two columns keep x
            matrix[2, 2] = 1.  # set 3D rot
        else:
            pass

    elif alignType == ALIGN_3D:
        flip = bool(numpy.linalg.det(matrix[0:3, 0:3]) < 0)
        if flip:
            matrix[0, :4] *= -1.  # now, invert first line including x
            matrix[3, 3] = 1.  # set 3D rot
        else:
            pass

    else:
        flip = bool(numpy.linalg.det(matrix[0:3, 0:3]) < 0)
        if flip:
            raise Exception("the det of the transformation matrix is "
                            "negative. This is not a valid transformation "
                            "matrix for Scipion.")
    shifts, angles = geometryFromMatrix(matrix, inverseTransform)
    alignmentRow.setValue(xmippLib.MDL_SHIFT_X, shifts[0])
    alignmentRow.setValue(xmippLib.MDL_SHIFT_Y, shifts[1])

    if is2D:
        angle = angles[0] + angles[2]
        alignmentRow.setValue(xmippLib.MDL_ANGLE_PSI,  angle)
    else:
        # if alignType == ALIGN_3D:
        alignmentRow.setValue(xmippLib.MDL_SHIFT_Z, shifts[2])
        alignmentRow.setValue(xmippLib.MDL_ANGLE_ROT,  angles[0])
        alignmentRow.setValue(xmippLib.MDL_ANGLE_TILT, angles[1])
        alignmentRow.setValue(xmippLib.MDL_ANGLE_PSI,  angles[2])
    alignmentRow.setValue(xmippLib.MDL_FLIP, flip)


def fillClasses(clsSet, updateClassCallback=None):
    """ Give an empty SetOfClasses (either 2D or 3D).
    Iterate over the input images and append to the corresponding class.
    It is important that each image has the classId properly set.
    """
    clsDict = {}  # Dictionary to store the (classId, classSet) pairs
    inputImages = clsSet.getImages()

    for img in inputImages:
        ref = img.getClassId()
        if ref is None:
            raise Exception('Particle classId is None!!!')

        # Register a new class set if the ref was not found.
        if ref not in clsDict:
            classItem = clsSet.ITEM_TYPE(objId=ref)
            rep = clsSet.REP_TYPE()
            classItem.setRepresentative(rep)
            clsDict[ref] = classItem
            classItem.copyInfo(inputImages)
            classItem.setAcquisition(inputImages.getAcquisition())
            if updateClassCallback is not None:
                updateClassCallback(classItem)
            clsSet.append(classItem)
        else:
            # Try to get the class set given its ref number
            classItem = clsDict[ref]
        classItem.append(img)

    for classItem in clsDict.values():
        clsSet.update(classItem)


# FIXME: USE THIS FUNCTION AS THE WAY TO CREATE CLASSES, REMOVE THE NEXT ONE
def createClassesFromImages2(inputImages, inputMd,
                             classesFn, ClassType, classLabel,
                             alignType, getClassFn=None,
                             preprocessImageRow=None):
    """ From an intermediate X.xmd file produced by xmipp, create
    the set of classes in which those images are classified.
    Params:
        inputImages: the SetOfImages that were initially classified by relion.
        inputMd: the filename metadata.
        classesFn: filename where to write the classes.
        ClassType: the output type of the classes set ( usually SetOfClass2D or
        3D )
        classLabel: label that is the class reference.
        classFnTemplate: the template to get the classes averages filenames
        iter: the iteration number, just used in Class template
    """
    mdIter = iterMdRows(inputMd)
    clsDict = {}  # Dictionary to store the (classId, classSet) pairs
    clsSet = ClassType(filename=classesFn)
    clsSet.setImages(inputImages)
    hasCtf = inputImages.hasCTF()
    sampling = inputImages.getSamplingRate()

    for img, row in izip(inputImages, mdIter):
        ref = row.getValue(xmippLib.MDL_REF)
        if ref is None:
            raise Exception('MDL_REF not found in metadata: %s' % inputMd)

        if ref not in clsDict:  # Register a new class set if the ref was not
                                # found.
            classItem = clsSet.ITEM_TYPE(objId=ref)
            if getClassFn is None:
                refFn = ''
            else:
                refFn = getClassFn(ref)
            refLocation = xmippToLocation(refFn)
            rep = clsSet.REP_TYPE()
            rep.setLocation(refLocation)
            rep.setSamplingRate(sampling)
            classItem.setRepresentative(rep)

            clsDict[ref] = classItem
            classItem.copyInfo(inputImages)
            classItem.setAlignment(alignType)
            classItem.setAcquisition(inputImages.getAcquisition())
            clsSet.append(classItem)
        else:
            # Try to get the class set given its ref number
            classItem = clsDict[ref]

        img.setTransform(rowToAlignment(row, alignType))
        classItem.append(img)

    for classItem in clsDict.values():
        clsSet.update(classItem)

    clsSet.write()
    return clsSet


# FIXME: remove this function and use previous one
def createClassesFromImages(inputImages, inputMd,
                            classesFn, ClassType, classLabel, classFnTemplate,
                            alignType, iter, preprocessImageRow=None):
    """ From an intermediate X.xmd file produced by xmipp, create
    the set of classes in which those images are classified.
    Params:
        inputImages: the SetOfImages that were initially classified by relion.
        inputMd: the filename metadata.
        classesFn: filename where to write the classes.
        ClassType: the output type of the classes set
                   (usually SetOfClass2D or 3D)
        classLabel: label that is the class reference.
        classFnTemplate: the template to get the classes averages filenames
        iter: the iteration number, just used in Class template
    """
    # We assume here that the volumes (classes3d) are in the same folder than
    #    imgsFn
    # rootDir here is defined to be used expanding locals()
    if "@" in inputMd:
        inputFn = inputMd.split('@')[1]
        tmpDir = os.path.dirname(inputFn)
    else:
        tmpDir = os.path.dirname(inputMd)

    def getClassFn(ref):
        args = {'rootDir': tmpDir, 'iter': iter, 'ref': ref}
        return classFnTemplate % args

    createClassesFromImages2(inputImages, inputMd,
                             classesFn, ClassType, classLabel,
                             alignType, getClassFn=getClassFn,
                             preprocessImageRow=preprocessImageRow)


def createItemMatrix(item, row, align):
    item.setTransform(rowToAlignment(row, alignType=align))


def readShiftsMovieAlignment(xmdFn):
    shiftsMd = md.MetaData(xmdFn)
    shiftsMd.removeDisabled()

    return (shiftsMd.getColumnValues(md.MDL_SHIFT_X),
            shiftsMd.getColumnValues(md.MDL_SHIFT_Y))


def writeShiftsMovieAlignment(movie, xmdFn, s0, sN):
    movieAlignment = movie.getAlignment()
    shiftListX, shiftListY = movieAlignment.getShifts()
    # Generating metadata for global shifts
    a0, aN = movieAlignment.getRange()
    globalShiftsMD = xmippLib.MetaData()
    alFrame = a0

    if s0 < a0:
        for i in range(s0, a0):
            objId = globalShiftsMD.addObject()
            imgFn = locationToXmipp(i, getMovieFileName(movie))
            globalShiftsMD.setValue(xmippLib.MDL_IMAGE, imgFn, objId)
            globalShiftsMD.setValue(xmippLib.MDL_SHIFT_X, 0.0, objId)
            globalShiftsMD.setValue(xmippLib.MDL_SHIFT_Y, 0.0, objId)

    for shiftX, shiftY in izip(shiftListX, shiftListY):
        if alFrame >= s0 and alFrame <= sN:
            objId = globalShiftsMD.addObject()
            imgFn = locationToXmipp(alFrame, getMovieFileName(movie))
            globalShiftsMD.setValue(xmippLib.MDL_IMAGE, imgFn, objId)
            globalShiftsMD.setValue(xmippLib.MDL_SHIFT_X, shiftX, objId)
            globalShiftsMD.setValue(xmippLib.MDL_SHIFT_Y, shiftY, objId)
        alFrame += 1

    if sN > aN:
        for j in range(aN, sN):
            objId = globalShiftsMD.addObject()
            imgFn = locationToXmipp(j+1, getMovieFileName(movie))
            globalShiftsMD.setValue(xmippLib.MDL_IMAGE, imgFn, objId)
            globalShiftsMD.setValue(xmippLib.MDL_SHIFT_X, 0.0, objId)
            globalShiftsMD.setValue(xmippLib.MDL_SHIFT_Y, 0.0, objId)

    globalShiftsMD.write(xmdFn)


def writeMovieMd(movie, outXmd, f1, fN, useAlignment=False):
    movieMd = md.MetaData()
    frame = movie.clone()
    firstFrame, lastFrame, frameIndex = movie.getFramesRange()

    if lastFrame == 0:
        # this condition is for old SetOfMovies, that has lastFrame = 0.
        frames = movie.getNumberOfFrames()
        if frames is not None:
            lastFrame = frames

    if f1 < firstFrame or fN > lastFrame:
        raise Exception("Frame range could not be greater"
                        " than the movie one.")

    ih = ImageHandler()

    if useAlignment:
        alignment = movie.getAlignment()
        if alignment is None:
            raise Exception("Can not write alignment for movie. ")
        a0, aN = alignment.getRange()
        if (firstFrame, lastFrame) != (a0, aN):
            raise Exception("Mismatch between alignment frames range and "
                            "movie frames range. ")
        shiftListX, shiftListY = alignment.getShifts()

    row = md.Row()
    stackIndex = frameIndex + (f1 - firstFrame)

    for i in range(f1, fN+1):
        frame.setIndex(stackIndex)
        row.setValue(md.MDL_IMAGE, ih.locationToXmipp(frame))

        if useAlignment:
            shiftIndex = i - firstFrame
            row.setValue(xmippLib.MDL_SHIFT_X, shiftListX[shiftIndex])
            row.setValue(xmippLib.MDL_SHIFT_Y, shiftListY[shiftIndex])

        row.addToMd(movieMd)
        stackIndex += 1

    movieMd.write(outXmd)


def createParamPhantomFile(filename, dimX, partSetMd, phFlip=False,
                           ctfCorr=False):
    f = open(filename, 'w')
    str = "# XMIPP_STAR_1 *\n#\ndata_block1\n_dimensions2D '%d %d'\n" % \
          (dimX, dimX)
    str += "_projAngleFile %s\n" % partSetMd
    str += "_ctfPhaseFlipped %d\n_ctfCorrected %d\n" % (phFlip, ctfCorr)
    str += "_applyShift 1\n_noisePixelLevel    '0 0'\n"
    f.write(str)
    f.close()
