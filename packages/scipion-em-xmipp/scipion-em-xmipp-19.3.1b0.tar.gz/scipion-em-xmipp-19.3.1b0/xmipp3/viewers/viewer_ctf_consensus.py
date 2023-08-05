# **************************************************************************
# *
# * Authors:     Roberto Marabini (roberto@cnb.csic.es)
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

from xmipp3.protocols.protocol_ctf_consensus import XmippProtCTFConsensus
from pyworkflow.em.viewers import EmPlotter, ObjectView
from pyworkflow.em.viewers.showj import MODE, MODE_MD, ORDER, VISIBLE
from pyworkflow.protocol.params import IntParam, LabelParam
from pyworkflow.viewer import DESKTOP_TKINTER, WEB_DJANGO, ProtocolViewer


class XmippCTFConsensusViewer(ProtocolViewer):
    """ This protocol computes the maximum resolution up to which two
     CTF estimations would be ``equivalent'', defining ``equivalent'' as having
      a wave aberration function shift smaller than 90 degrees
    """
    _label = 'viewer CTF Consensus'
    _environments = [DESKTOP_TKINTER, WEB_DJANGO]
    _targets = [XmippProtCTFConsensus]
    _memory = False
    resolutionThresholdOLD = -1
    # temporary metadata file with ctf that has some resolution greathan than X
    tmpMetadataFile = 'viewersTmp.sqlite'

    def _defineParams(self, form):
        form.addSection(label='Visualization')
        # group = form.addGroup('Overall results')
        form.addParam('visualizePairs', LabelParam,
                      label="Visualize ctf + max resolution.",
                      help="""Reference CTF plus a new column with
                      resolution up to which reference CTF and target
                      reference are similar""")
        form.addParam('visualizeHistogram', IntParam, default=10,
                      label="Visualize Histogram (Bin size)",
                      help="Histogram of the resolution at which two methods"
                           " are equivalent")

    def _getVisualizeDict(self):
        return {
                 'visualizePairs': self._visualizePairs,
                 'visualizeHistogram': self._visualizeHistogram
                }

    def _visualizePairs(self, e=None):
        views = []

        # display metadata with selected variables
        labels = 'id enabled _psdFile _micObj_filename _resolution ' \
                 '_xmipp_consensus_resolution _xmipp_discrepancy_astigmatism' \
                 ' _defocusU _defocusV _defocusAngle'
        if hasattr(self.protocol, "outputCTF"):
            views.append(ObjectView(
                self._project, self.protocol.strId(),
                self.protocol.outputCTF.getFileName(),
                viewParams={MODE: MODE_MD, ORDER: labels, VISIBLE: labels}))
        if hasattr(self.protocol, "outputCTFDiscarded"):
            views.append(ObjectView(
                self._project, self.protocol.strId(),
                self.protocol.outputCTFDiscarded.getFileName(),
                viewParams={MODE: MODE_MD, ORDER: labels, VISIBLE: labels}))
        return views

    def _visualizeHistogram(self, e=None):
        views = []
        numberOfBins = self.visualizeHistogram.get()
        if hasattr(self.protocol, "outputCTF"):
            numberOfBins = min(numberOfBins, self.protocol.outputCTF.getSize())
            plotter = EmPlotter()
            plotter.createSubPlot("Resolution Discrepancies histogram",
                                  "Resolution (A)", "# of Comparisons")
            resolution = [ctf.getResolution() for ctf in
                          self.protocol.outputCTF]
            plotter.plotHist(resolution, nbins=numberOfBins)
            views.append(plotter)

        if hasattr(self.protocol, "outputCTFDiscarded"):
            numberOfBins = min(numberOfBins,
                               self.protocol.outputCTFDiscarded.getSize())
            plotter = EmPlotter()
            plotter.createSubPlot(
                "Resolution Discrepancies histogram (discarded)",
                "Resolution (A)", "# of Comparisons")
            resolution = [ctf.getResolution() for ctf in
                          self.protocol.outputCTFDiscarded]
            plotter.plotHist(resolution, nbins=numberOfBins)
            views.append(plotter)
        return views