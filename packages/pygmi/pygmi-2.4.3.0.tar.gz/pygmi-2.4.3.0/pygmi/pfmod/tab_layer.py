# -----------------------------------------------------------------------------
# Name:        tab_layer.py (part of PyGMI)
#
# Author:      Patrick Cole
# E-Mail:      pcole@geoscience.org.za
#
# Copyright:   (c) 2013 Council for Geoscience
# Licence:     GPL-3.0
#
# This file is part of PyGMI
#
# PyGMI is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyGMI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------
""" Layer Display Tab Routines """

from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib import cm
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
import pygmi.pfmod.misc as misc


class LayerDisplay(object):
    """ Widget class to call the main interface """
    def __init__(self, parent):
        self.parent = parent
        self.lmod = parent.lmod1
        self.grid_stretch = 'linear'
        self.grid3txt = 'Calculated Magnetics'

        self.grid3 = self.lmod.griddata['Calculated Magnetics']

        self.userint = QtWidgets.QWidget()

        self.mmc = MyMplCanvas(self, self.lmod)
        self.mpl_toolbar = NavigationToolbar2QT(self.mmc, self.userint)

        self.label_altitude = QtWidgets.QLabel()
        self.sb_model_layer = QtWidgets.QSpinBox()
        self.hslider_layer = QtWidgets.QSlider()
        self.combo_grid3 = QtWidgets.QComboBox()
        self.hs_model_opacity = QtWidgets.QSlider()
        self.sb_layer_linethick = QtWidgets.QSpinBox()
        self.lw_editor_defs = QtWidgets.QListWidget()
        self.pb_layer_rcopy = QtWidgets.QPushButton()

        self.setupui()

    def setupui(self):
        """ Setup UI """
        gridlayout = QtWidgets.QGridLayout(self.userint)

        gtmp = ['Calculated Magnetics', 'Calculated Gravity']

        self.lw_editor_defs.setFixedWidth(220)
        self.sb_model_layer.setWrapping(True)
        self.sb_model_layer.setMinimum(0)
        self.sb_model_layer.setMaximum(1000)
        self.sb_model_layer.setProperty("value", 0)

        sizepolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)

        self.hslider_layer.setSizePolicy(sizepolicy)
        self.hslider_layer.setOrientation(QtCore.Qt.Horizontal)
        self.hs_model_opacity.setSizePolicy(sizepolicy)
        self.hs_model_opacity.setMaximum(100)
        self.hs_model_opacity.setProperty("value", 100)
        self.hs_model_opacity.setOrientation(QtCore.Qt.Horizontal)
        self.hs_model_opacity.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sb_layer_linethick.setMinimum(1)
        self.sb_layer_linethick.setMaximum(1000)
        self.sb_model_layer.setMaximum(self.lmod.numz-1)
        self.combo_grid3.addItems(gtmp)
        self.combo_grid3.setCurrentIndex(0)

        self.label_altitude.setText("Altitude: 0")
        self.sb_model_layer.setPrefix("Model Layer: ")
        self.hslider_layer.setToolTip("Model Layer")
        self.hs_model_opacity.setToolTip("Model Opacity")
        self.sb_layer_linethick.setPrefix("Line Thickness: ")
        self.pb_layer_rcopy.setText("Ranged Copy")

        gridlayout.addWidget(self.mpl_toolbar, 0, 0, 1, 1)
        gridlayout.addWidget(self.mmc, 1, 0, 8, 1)
        gridlayout.addWidget(self.label_altitude, 0, 1, 1, 1)
        gridlayout.addWidget(self.sb_model_layer, 1, 1, 1, 1)
        gridlayout.addWidget(self.hslider_layer, 2, 1, 1, 1)
        gridlayout.addWidget(self.combo_grid3, 3, 1, 1, 1)
        gridlayout.addWidget(self.hs_model_opacity, 4, 1, 1, 1)
        gridlayout.addWidget(self.lw_editor_defs, 5, 1, 1, 1)
        gridlayout.addWidget(self.sb_layer_linethick, 6, 1, 1, 1)
        gridlayout.addWidget(self.pb_layer_rcopy, 7, 1, 1, 1)

        self.sb_model_layer.valueChanged.connect(self.sb_laynum)
        self.combo_grid3.currentIndexChanged.connect(self.combo)
        self.lw_editor_defs.currentItemChanged.connect(self.change_defs)
        self.hslider_layer.valueChanged.connect(self.layer_hs)
        self.pb_layer_rcopy.clicked.connect(self.rcopy)
        self.sb_layer_linethick.valueChanged.connect(self.setwidth)
        self.hs_model_opacity.valueChanged.connect(self.sb_laynum)

    def change_defs(self):
        """ List box in layer tab for definitions """
        i = self.lw_editor_defs.currentRow()
        if i == -1:
            misc.update_lith_lw(self.lmod, self.lw_editor_defs)
            i = 0
        itxt = str(self.lw_editor_defs.item(i).text())
        if itxt not in self.lmod.lith_list:
            return

        lith = self.lmod.lith_list[itxt]
        self.mmc.curmodel = lith.lith_index

    def combo(self):
        """ Combo box to choose grid 3 """
        ctxt = str(self.combo_grid3.currentText())
        if ctxt == '':
            return
        self.grid3txt = ctxt
        self.grid3 = self.lmod.griddata[ctxt]
        self.update_model_plot()

    def layer_hs(self, hval):
        """ Horizontal slider to change the layer """
        perc = hval / float(self.hslider_layer.maximum())
        self.sb_model_layer.setValue(int((self.lmod.numz-1)*perc))
        self.sb_laynum()

    def rcopy(self):
        """ Do a ranged copy on a layer """
        self.update_model()
        misc.rcopy_dialog(self.lmod, islayer=True, is_ew=self.lmod.is_ew)

    def sb_laynum(self):
        """ This increases or decreases the model layer """
        self.update_model()
        self.lmod.curlayer = self.sb_model_layer.value()
        alt = self.lmod.zrange[1]-self.lmod.curlayer*self.lmod.d_z
        self.label_altitude.setText('Altitude: '+str(alt))

        gtmp = self.lmod.lith_index[:, :, self.lmod.curlayer].T.copy()
        opac = self.hs_model_opacity.value()/100.
        self.mmc.opac = opac
        self.mmc.slide_grid(gtmp, self.grid3)

    def update_combos(self):
        """ This updates combos """
        tmp = list(self.lmod.griddata.keys())
        self.combo_grid3.blockSignals(True)

        self.combo_grid3.clear()
        self.combo_grid3.addItems(tmp)
        self.combo_grid3.setCurrentIndex(tmp.index(self.grid3txt))

        self.combo_grid3.blockSignals(False)

    def update_model_plot(self):
        """ This updates some of the plotting stuff """
        self.lmod.curlayer = self.sb_model_layer.value()
        alt = self.lmod.zrange[1]-self.lmod.curlayer*self.lmod.d_z
        self.label_altitude.setText('Altitude: '+str(alt))

        gtmp = self.lmod.lith_index[:, :, self.lmod.curlayer].T.copy()

        left = self.lmod.xrange[0]
        right = self.lmod.xrange[1]
        bottom = self.lmod.yrange[0]
        top = self.lmod.yrange[1]
        extent = (left, right, bottom, top)
        opac = self.hs_model_opacity.value()/100.

        self.mmc.init_grid(gtmp, self.grid3, extent, opac)

        if self.lmod.is_ew:
            xys = self.lmod.yrange[0]+self.lmod.curprof*self.lmod.dxy
            self.mmc.init_line(self.lmod.xrange, [xys, xys])
        else:
            xys = self.lmod.xrange[0]+self.lmod.curprof*self.lmod.dxy
            self.mmc.init_line([xys, xys], self.lmod.yrange)

    def update_model(self):
        """ Updates the model from the graph """
        self.lmod.lith_index[:, :, self.lmod.curlayer] = \
            self.mmc.mdata.T.copy()

    def setwidth(self, width):
        """ Sets the width of the edits on the layer view """
        self.mmc.mywidth = width

    def tab_activate(self):
        """ Runs when the tab is activated """
        self.lmod = self.parent.lmod1
        self.mmc.set_limits(self.lmod)
        self.mmc.lmod = self.lmod
        self.update_combos()
        misc.update_lith_lw(self.lmod, self.lw_editor_defs)
        self.sb_model_layer.setMaximum(self.lmod.numz-1)
        self.combo()


class MyMplCanvas(FigureCanvas):
    """
    Canvas for the actual plot

    Attributes
    ----------
    """
    def __init__(self, parent, lmod):
        fig = Figure()
        FigureCanvas.__init__(self, fig)

        self.myparent = parent
        self.lmod = lmod
        self.cbar = cm.jet
        self.curmodel = 0
        self.mywidth = 1
        self.xold = None
        self.yold = None
        self.press = False
        self.newline = False
        self.mdata = np.zeros([100, 100])
        self.opac = 1.0
        self.xlims = None
        self.ylims = None

# Events
        self.figure.canvas.mpl_connect('motion_notify_event', self.move)
        self.figure.canvas.mpl_connect('button_press_event', self.button_press)
        self.figure.canvas.mpl_connect('button_release_event',
                                       self.button_release)

# Initial Images
        self.axes = fig.add_subplot(111)
        self.axes.xaxis.set_label_text("Eastings (m)")
        self.axes.yaxis.set_label_text("Northings (m)")
        self.ims2 = self.axes.imshow(self.mdata, cmap=self.cbar,
                                     interpolation='nearest')
        self.ims = self.axes.imshow(self.cbar(self.mdata),
                                    interpolation='nearest')
        self.figure.canvas.draw()

        self.bbox = self.figure.canvas.copy_from_bbox(self.axes.bbox)

        self.prf = self.axes.plot([0, 1], [0, 1])
        self.figure.canvas.draw()
        self.lbbox = self.figure.canvas.copy_from_bbox(self.axes.bbox)

    def button_press(self, event):
        """ Button press """
        nmode = self.axes.get_navigate_mode()
        if event.button == 1 and nmode is None:
            self.press = True
            self.newline = True
            self.move(event)

    def button_release(self, event):
        """ Button press """
        if event.button == 1:
            self.press = False
            self.myparent.update_model()

    def move(self, event):
        """ Mouse is moving """
        if self.figure.canvas.toolbar._active is None:
            vlim = self.axes.viewLim
            xptp = self.lmod.xrange[1]-self.lmod.xrange[0]
            yptp = self.lmod.yrange[1]-self.lmod.yrange[0]
            if xptp > 10000 or yptp > 10000:
                xptp /= 1000
                yptp /= 1000
            tmp0 = self.axes.transData.transform((vlim.x0, vlim.y0))
            tmp1 = self.axes.transData.transform((vlim.x1, vlim.y1))
            width, height = tmp1-tmp0
            width /= self.mdata.shape[1]
            height /= self.mdata.shape[0]

            width *= xptp/vlim.width
            height *= yptp/vlim.height

            cwidth = (2*self.mywidth-1)
            cb = QtGui.QBitmap(cwidth*width, cwidth*height)
            cb.fill(QtCore.Qt.color1)
            self.setCursor(QtGui.QCursor(cb))

        if self.axes.xaxis.get_label_text().find('km') > -1:
            cdiv = 1000.
        else:
            cdiv = 1.

        dxy = self.lmod.dxy/cdiv
        xmin = self.lmod.xrange[0]/cdiv
        ymin = self.lmod.yrange[0]/cdiv

        if event.inaxes == self.axes and self.press is True:
            col = int((event.xdata - xmin)/dxy)+1
            row = int((event.ydata - ymin)/dxy)+1

            xdata = col
            ydata = row

            if self.newline is True:
                self.newline = False
                self.set_mdata(xdata, ydata)
            elif xdata != self.xold:
                mmm = float(ydata-self.yold)/(xdata-self.xold)
                ccc = ydata - mmm * xdata
                x_1 = min([self.xold, xdata])
                x_2 = max([self.xold, xdata])
                for i in range(x_1+1, x_2+1):
                    jold = int(mmm*(i-1)+ccc)
                    jnew = int(mmm*i+ccc)
                    if jold > jnew:
                        jold, jnew = jnew, jold
                    for j in range(jold, jnew+1):
                        self.set_mdata(i, j)

            elif ydata != self.yold:
                y_1 = min([self.yold, ydata])
                y_2 = max([self.yold, ydata])
                for j in range(y_1, y_2+1):
                    self.set_mdata(xdata, j)

            self.xold = xdata
            self.yold = ydata

            self.slide_grid(self.mdata)

    def set_mdata(self, xdata, ydata):
        """ Routine to 'draw' the line on mdata """
        gheight = self.mdata.shape[0]
        gwidth = self.mdata.shape[1]

        width = self.mywidth-1  # 'pen' width
        xstart = xdata-width-1
        xend = xdata+width
        ystart = ydata-width-1
        yend = ydata+width
        if xstart < 0:
            xstart = 0
        if xend > gwidth:
            xend = gwidth
        if ystart < 0:
            ystart = 0
        if yend > gheight:
            yend = gheight

        if xstart < xend and ystart < yend:
            mtmp = self.mdata[ystart:yend, xstart:xend]
            mtmp[mtmp != -1] = self.curmodel

    def luttodat(self, dat):
        """ lut to dat grid """
        mlut = self.lmod.mlut
        tmp = np.zeros([dat.shape[0], dat.shape[1], 4])

        for i in np.unique(dat):
            if i == -1:
                ctmp = [0, 0, 0, 0]
            else:
                ctmp = np.array(mlut[i]+[255])/255.

            tmp[dat[::-1] == i] = ctmp

        return tmp

    def init_grid(self, dat, dat2, extent, opac):
        """ Updates the single color map """
        left, right, bottom, top = extent

        if (right-left) > 10000 or (top-bottom) > 10000:
            self.axes.xaxis.set_label_text("Eastings (km)")
            self.axes.yaxis.set_label_text("Northings (km)")
            left /= 1000.
            right /= 1000.
            top /= 1000.
            bottom /= 1000.
            extent = (left, right, bottom, top)
        else:
            self.axes.xaxis.set_label_text("Eastings (m)")
            self.axes.yaxis.set_label_text("Northings (m)")

        self.mdata = dat
        tmp = self.luttodat(dat)

        self.ims.set_visible(False)
        self.ims.set_data(tmp)
        self.ims.set_extent(extent)
        self.ims.set_alpha(opac)

        self.ims2.set_data(dat2.data)
        self.ims2.set_extent(self.dat_extent(dat2))
        if self.xlims is not None:
            self.axes.set_xlim(self.xlims)
            self.axes.set_ylim(self.ylims)
        self.ims2.set_clim(dat2.data.min(), dat2.data.max())

        self.figure.canvas.draw()
        QtWidgets.QApplication.processEvents()
        self.bbox = self.figure.canvas.copy_from_bbox(self.axes.bbox)

        self.ims.set_visible(True)
        self.figure.canvas.draw()
        self.lbbox = self.figure.canvas.copy_from_bbox(self.axes.bbox)
        self.slide_grid(dat, dat2)  # used to get rid of extra line

    def slide_grid(self, dat, dat2=None):
        """ Slider """
        opac = self.opac

        tmp = self.luttodat(dat)
        self.ims.set_data(tmp)
        self.ims.set_alpha(opac)
        if dat2 is not None:
            self.ims2.set_data(dat2.data)

        self.figure.canvas.restore_region(self.bbox)
        self.axes.draw_artist(self.ims2)
        self.axes.draw_artist(self.ims)
        self.figure.canvas.update()
        self.mdata = dat
        self.lbbox = self.figure.canvas.copy_from_bbox(self.axes.bbox)
        self.axes.draw_artist(self.prf[0])
        self.figure.canvas.update()

    def init_line(self, xrng, yrng):
        """ Updates the line position """
        if self.axes.xaxis.get_label_text().find('km') > -1:
            xrng = [xrng[0]/1000., xrng[1]/1000.]
            yrng = [yrng[0]/1000., yrng[1]/1000.]

        self.prf[0].set_data([xrng, yrng])
        self.figure.canvas.restore_region(self.lbbox)
        self.axes.draw_artist(self.prf[0])
        self.figure.canvas.update()

    def dat_extent(self, dat):
        """ Gets the extend of the dat variable """
        left = dat.tlx
        top = dat.tly
        right = left + dat.cols*dat.xdim
        bottom = top - dat.rows*dat.ydim

        if (right-left) > 10000 or (top-bottom) > 10000:
            self.axes.xaxis.set_label_text("Eastings (km)")
            self.axes.yaxis.set_label_text("Northings (km)")
            left /= 1000.
            right /= 1000.
            top /= 1000.
            bottom /= 1000.
        else:
            self.axes.xaxis.set_label_text("Eastings (m)")
            self.axes.yaxis.set_label_text("Northings (m)")

        return (left, right, bottom, top)

    def set_limits(self, lmod):
        """ Sets limits for the axes """
        left, right = lmod.xrange
        bottom, top = lmod.yrange
        if (right-left) > 10000 or (top-bottom) > 10000:
            left /= 1000.
            right /= 1000.
            top /= 1000.
            bottom /= 1000.

        self.xlims = (left, right)
        self.ylims = (bottom, top)
        self.axes.set_xlim(self.xlims)
        self.axes.set_ylim(self.ylims)
