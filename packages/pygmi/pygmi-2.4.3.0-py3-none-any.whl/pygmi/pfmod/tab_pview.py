# -----------------------------------------------------------------------------
# Name:        tab_pview.py (part of PyGMI)
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
""" Profile Display Tab Routines """

import os
from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np
import scipy.ndimage as ndimage

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib import cm
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from pygmi.pfmod import misc


class ProfileDisplay(object):
    """ Widget class to call the main interface """
    def __init__(self, parent):
        self.parent = parent
        self.lmod1 = parent.lmod1
        self.lmod2 = parent.lmod2
        self.showtext = parent.showtext
        self.pbar = self.parent.pbar_sub
        self.xnodes = self.lmod1.custprofx
        self.ynodes = self.lmod1.custprofy
        self.curprof = 0
        self.pcntmax = len(self.xnodes)-1
        self.viewmagnetics = True

        self.userint = QtWidgets.QWidget()

        self.mmc = MyMplCanvas(self, self.lmod1)
        self.mpl_toolbar = NavigationToolbar2QT(self.mmc, self.userint)

        self.sb_profnum2 = QtWidgets.QSpinBox()
        self.hslider_profile2 = QtWidgets.QSlider()
        self.combo_profpic = QtWidgets.QComboBox()
        self.hs_ppic_opacity = QtWidgets.QSlider()

        self.rb_axis_datamax = QtWidgets.QRadioButton()
        self.rb_axis_profmax = QtWidgets.QRadioButton()
        self.rb_axis_calcmax = QtWidgets.QRadioButton()

        self.sb_profile_linethick = QtWidgets.QSpinBox()
        self.gridlayout_20 = QtWidgets.QGridLayout()
        self.lw_prof_defs = QtWidgets.QListWidget()

        self.pb_add_prof = QtWidgets.QPushButton()
        self.pb_export_csv = QtWidgets.QPushButton()

        self.setupui()

    def setupui(self):
        """ Setup UI """
        gridlayout = QtWidgets.QGridLayout(self.userint)
        groupbox = QtWidgets.QGroupBox()
        verticallayout = QtWidgets.QVBoxLayout(groupbox)

        self.sb_profnum2.setWrapping(True)
        self.sb_profnum2.setMaximum(999999999)

        sizepolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                       QtWidgets.QSizePolicy.Fixed)
        self.hslider_profile2.setSizePolicy(sizepolicy)
        self.hs_ppic_opacity.setSizePolicy(sizepolicy)

        self.lw_prof_defs.setFixedWidth(220)
        self.hslider_profile2.setOrientation(QtCore.Qt.Horizontal)
        self.hs_ppic_opacity.setMaximum(255)
        self.hs_ppic_opacity.setProperty("value", 255)
        self.hs_ppic_opacity.setOrientation(QtCore.Qt.Horizontal)
        self.hs_ppic_opacity.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sb_profile_linethick.setMinimum(1)
        self.sb_profile_linethick.setMaximum(1000)
        self.rb_axis_datamax.setChecked(True)

        gridlayout.addWidget(self.mpl_toolbar, 0, 0, 1, 1)
        gridlayout.addWidget(self.mmc, 1, 0, 7, 1)
        gridlayout.addWidget(self.sb_profnum2, 0, 1, 1, 1)
        gridlayout.addWidget(self.hslider_profile2, 1, 1, 1, 1)
        gridlayout.addWidget(self.combo_profpic, 2, 1, 1, 1)
        gridlayout.addWidget(self.hs_ppic_opacity, 3, 1, 1, 1)
        gridlayout.addWidget(self.lw_prof_defs, 4, 1, 1, 1)
        gridlayout.addWidget(self.sb_profile_linethick, 5, 1, 1, 1)
        gridlayout.addWidget(groupbox, 6, 1, 1, 1)
        gridlayout.addWidget(self.pb_add_prof, 7, 1, 1, 1)
        gridlayout.addWidget(self.pb_export_csv, 8, 1, 1, 1)

        verticallayout.addWidget(self.rb_axis_datamax)
        verticallayout.addWidget(self.rb_axis_profmax)
        verticallayout.addWidget(self.rb_axis_calcmax)

        groupbox.setTitle("Profile Y-Axis Scale")
        self.sb_profnum2.setPrefix("Custom Profile: ")
        self.pb_add_prof.setText("Add Custom Profile")
        self.pb_export_csv.setText("Export Profile")
        self.rb_axis_datamax.setText("Scale to dataset maximum")
        self.rb_axis_profmax.setText("Scale to profile maximum")
        self.rb_axis_calcmax.setText("Scale to calculated maximum")
        self.sb_profile_linethick.setPrefix("Line Thickness: ")

    # Buttons etc
        self.sb_profile_linethick.valueChanged.connect(self.setwidth)
        self.lw_prof_defs.currentItemChanged.connect(self.change_defs)
        self.pb_add_prof.clicked.connect(self.addprof)
        self.hslider_profile2.valueChanged.connect(self.hprofnum)
        self.hslider_profile2.sliderReleased.connect(self.hprofnum)
        self.sb_profnum2.valueChanged.connect(self.sprofnum)
        self.rb_axis_calcmax.clicked.connect(self.rb_plot_scale)
        self.rb_axis_profmax.clicked.connect(self.rb_plot_scale)
        self.rb_axis_datamax.clicked.connect(self.rb_plot_scale)
        self.pb_export_csv.clicked.connect(self.export_csv)
        self.hs_ppic_opacity.sliderMoved.connect(self.profpic_hs)
        self.combo_profpic.currentIndexChanged.connect(self.profpic_hs)

    def addprof(self):
        """ add another profile """
        self.update_model()
        (tx0, okay) = QtWidgets.QInputDialog.getDouble(
            self.parent, 'Add Custom Profile',
            'Please enter first x coordinate', self.lmod1.xrange[0])
        if not okay:
            return
        (ty0, okay) = QtWidgets.QInputDialog.getDouble(
            self.parent, 'Add Custom Profile',
            'Please enter first y coordinate', self.lmod1.yrange[0])
        if not okay:
            return
        (tx1, okay) = QtWidgets.QInputDialog.getDouble(
            self.parent, 'Add Custom Profile',
            'Please enter last x coordinate', self.lmod1.xrange[-1])
        if not okay:
            return
        (ty1, okay) = QtWidgets.QInputDialog.getDouble(
            self.parent, 'Add Custom Profile',
            'Please enter last y coordinate', self.lmod1.yrange[-1])
        if not okay:
            return

        self.pcntmax += 1
        self.xnodes[self.pcntmax] = [float(tx0), float(tx1)]
        self.ynodes[self.pcntmax] = [float(ty0), float(ty1)]

        self.hslider_profile2.valueChanged.disconnect()
        self.combo_profpic.currentIndexChanged.disconnect()
        self.sb_profnum2.valueChanged.disconnect()

        self.hslider_profile2.setMaximum(self.pcntmax)
        self.sb_profnum2.setMaximum(self.pcntmax)

        self.sb_profnum2.valueChanged.connect(self.sprofnum)
        self.hslider_profile2.valueChanged.connect(self.hprofnum)
        self.combo_profpic.currentIndexChanged.connect(self.profpic_hs)

    def change_defs(self):
        """ List box in profile tab for definitions """

        i = self.lw_prof_defs.currentRow()
        if i == -1:
            misc.update_lith_lw(self.lmod1, self.lw_prof_defs)
            i = 0
        itxt = str(self.lw_prof_defs.item(i).text())

        if itxt not in self.lmod1.lith_list:
            return

        lith = self.lmod1.lith_list[itxt]
        self.mmc.curmodel = lith.lith_index

    def change_model(self, slide=False):
        """ Change Model """

        bottom = self.lmod1.zrange[0]
        top = self.lmod1.zrange[1]

        data = self.lmod1.griddata['Calculated Gravity']
        xxx, yyy, right = self.cp_init(data)

        tmp = np.transpose([xxx, yyy]).astype(int)
        self.mmc.crd = tmp

        x = np.array(xxx).astype(int)
        y = np.array(yyy).astype(int)

        gtmp = []
        for i in range(self.lmod1.numz):
            gtmp.append(self.lmod1.lith_index[x, y, i])

        gtmp = np.array(gtmp[::-1])
    # First we plot the model stuff
        left = 0

        extent = (left, right, bottom, top)

        ctxt = str(self.combo_profpic.currentText())
        if len(self.lmod1.profpics) > 0 and ctxt != u'':
            gtmpl = self.lmod1.profpics[ctxt]
            opac = self.hs_ppic_opacity.value()/self.hs_ppic_opacity.maximum()
        else:
            gtmpl = None
            opac = 1.0

        if slide is True:
            self.mmc.slide_grid(gtmp, gtmpl, opac)
        else:
            self.mmc.init_grid(gtmp, extent, gtmpl, opac)

    def cp_init(self, data):
        """ Initializes stuff for custom profile """
        x_0, x_1 = self.xnodes[self.curprof]
        y_0, y_1 = self.ynodes[self.curprof]

        bly = data.tly-data.ydim*data.rows
        x_0 = (x_0-data.tlx)/data.xdim
        x_1 = (x_1-data.tlx)/data.xdim
        y_0 = (y_0-bly)/data.ydim
        y_1 = (y_1-bly)/data.ydim
        rcell = int(np.sqrt((x_1-x_0)**2+(y_1-y_0)**2))
        rdist = np.sqrt((data.xdim*(x_1-x_0))**2+(data.ydim*(y_1-y_0))**2)

        xxx = np.linspace(x_0, x_1, rcell, False)
        yyy = np.linspace(y_0, y_1, rcell, False)

        return xxx, yyy, rdist

    def export_csv(self):
        """ Export Profile to csv """
        self.parent.pbars.resetall()
        filename, filt = QtWidgets.QFileDialog.getSaveFileName(
            self.parent, 'Save File', '.', 'Comma separated values (*.csv)')
        if filename == '':
            return
        os.chdir(filename.rpartition('/')[0])

        maggrid = self.lmod1.griddata['Calculated Magnetics'].data
        grvgrid = self.lmod1.griddata['Calculated Gravity'].data
        curprof = self.curprof

        cmag = maggrid[-curprof-1]
        cgrv = grvgrid[-curprof-1]
        xrng = (np.arange(cmag.shape[0])*self.lmod1.dxy +
                self.lmod1.xrange[0]+self.lmod1.dxy/2.)
        yrng = np.zeros_like(xrng)+self.lmod1.dxy/2.

        newdata = np.transpose([xrng, yrng, cgrv, cmag])

        fno = open(filename, 'wb')
        fno.write(b'"x","y","Gravity","Magnetics"\n')
        np.savetxt(fno, newdata, delimiter=',')
        fno.close()
        self.parent.pbars.incr()
        self.showtext('Profile save complete')

    def hprofnum(self):
        """ Routine to change a profile from spinbox"""
        self.sb_profnum2.setValue(self.hslider_profile2.sliderPosition())
        self.profnum()

    def profpic_hs(self):
        """ Horizontal slider to change the profile """
        self.update_model()
        self.change_model(slide=True)
        self.update_plot(slide=True)

    def profnum(self):
        """ Routine to change a profile from spinbox"""
        self.update_model()

        self.curprof = self.sb_profnum2.value()
        self.change_model(slide=False)
        self.update_plot(slide=False)  # was True

    def sprofnum(self):
        """ Routine to change a profile from spinbox"""
        self.hslider_profile2.setValue(self.sb_profnum2.value())
        self.profnum()

    def rb_plot_scale(self):
        """ plot scale """
        self.change_model()
        self.update_plot()
        self.mpl_toolbar.update()

    def tab_activate(self):
        """ Runs when the tab is activated """
        self.lmod1 = self.parent.lmod1
        self.mmc.lmod = self.lmod1

        self.xnodes = self.lmod1.custprofx
        self.ynodes = self.lmod1.custprofy
        self.pcntmax = len(self.xnodes)-1

        misc.update_lith_lw(self.lmod1, self.lw_prof_defs)

        self.hslider_profile2.valueChanged.disconnect()
        self.combo_profpic.currentIndexChanged.disconnect()
        self.sb_profnum2.valueChanged.disconnect()

        self.hslider_profile2.setMinimum(0)
        self.hslider_profile2.setMaximum(self.pcntmax)
        self.sb_profnum2.setMaximum(self.pcntmax)

        if len(self.lmod1.profpics) > 0:
            self.combo_profpic.clear()
            self.combo_profpic.addItems(list(self.lmod1.profpics.keys()))
            self.combo_profpic.setCurrentIndex(0)

        self.change_model()  # needs to happen before profnum set value
        self.sb_profnum2.setValue(self.curprof)
        self.update_plot()
        self.sb_profnum2.valueChanged.connect(self.sprofnum)
        self.hslider_profile2.valueChanged.connect(self.hprofnum)
        self.combo_profpic.currentIndexChanged.connect(self.profpic_hs)

    def update_model(self):
        """ Update model itself """

        data = self.lmod1.griddata['Calculated Gravity']
        xxx, yyy = self.cp_init(data)[:2]

        gtmp = self.mmc.mdata[::-1].T.copy()
        rows, cols = gtmp.shape

        for j in range(cols):
            for i in range(rows):
                self.lmod1.lith_index[int(xxx[i]), int(yyy[i]), j] = gtmp[i, j]

    def update_plot(self, slide=False):
        """ Update the profile on the model view """

# Display the calculated profile
        data = None

        if self.viewmagnetics:
            if 'Calculated Magnetics' in self.lmod1.griddata:
                data = self.lmod1.griddata['Calculated Magnetics']
            self.mmc.ptitle = 'Magnetic Intensity: '
            self.mmc.punit = 'nT'
            regtmp = 0.0
        else:
            if 'Calculated Gravity' in self.lmod1.griddata:
                data = self.lmod1.griddata['Calculated Gravity']
            self.mmc.ptitle = 'Gravity: '
            self.mmc.punit = 'mGal'
            regtmp = self.lmod1.gregional

        x_0, x_1 = self.xnodes[self.curprof]
        y_0, y_1 = self.ynodes[self.curprof]
        self.mmc.ptitle += str((x_0, y_0)) + ' to ' + str((x_1, y_1))

        if data is not None:
            xxx, yyy, rdist = self.cp_init(data)

            self.mmc.xlabel = "Eastings (m)"
            tmprng = np.linspace(0, rdist, len(xxx), False)
            tmpprof = ndimage.map_coordinates(data.data[::-1], [yyy, xxx],
                                              order=1, cval=np.nan)
            tmprng = tmprng[np.logical_not(np.isnan(tmpprof))]
            tmpprof = tmpprof[np.logical_not(np.isnan(tmpprof))]+regtmp
            extent = [0, rdist]

        if self.rb_axis_calcmax.isChecked():
            extent = list(extent)+[data.min()+regtmp, data.max()+regtmp]
        else:
            extent = list(extent)+[tmpprof.min(), tmpprof.max()]

# Load in observed data - if there is any
        data2 = None
        tmprng2 = None
        tmpprof2 = None
        if 'Magnetic Dataset' in self.lmod1.griddata and self.viewmagnetics:
            data2 = self.lmod1.griddata['Magnetic Dataset']
        elif ('Gravity Dataset' in self.lmod1.griddata and
              not self.viewmagnetics):
            data2 = self.lmod1.griddata['Gravity Dataset']

        if data2 is not None:
            xxx, yyy, rdist = self.cp_init(data2)

            tmprng2 = np.linspace(0, rdist, len(xxx), False)
            tmpprof2 = ndimage.map_coordinates(data2.data[::-1], [yyy, xxx],
                                               order=1, cval=np.nan)

            tmprng2 = tmprng2[np.logical_not(np.isnan(tmpprof2))]
            tmpprof2 = tmpprof2[np.logical_not(np.isnan(tmpprof2))]

            if self.rb_axis_datamax.isChecked() or len(tmpprof2) == 0:
                extent[2:] = [data2.data.min(), data2.data.max()]
            elif self.rb_axis_profmax.isChecked():
                extent[2:] = [tmpprof2.min(), tmpprof2.max()]

        if slide is True:
            self.mmc.slide_plot(tmprng, tmpprof, tmprng2, tmpprof2)
        else:
            self.mmc.init_plot(tmprng, tmpprof, extent, tmprng2, tmpprof2)

    def setwidth(self, width):
        """ Sets the width of the edits on the profile view """

        self.mmc.mywidth = width


class MyMplCanvas(FigureCanvas):
    """This is a QWidget"""
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
        self.mdata = np.zeros([10, 100])
        self.ptitle = ''
        self.punit = ''
        self.xlabel = 'Eastings (m)'
        self.plotisinit = False
        self.crd = None

# Events
        self.figure.canvas.mpl_connect('motion_notify_event', self.move)
        self.figure.canvas.mpl_connect('button_press_event', self.button_press)
        self.figure.canvas.mpl_connect('button_release_event',
                                       self.button_release)

# Initial Images
        self.paxes = fig.add_subplot(211)
        self.paxes.yaxis.set_label_text("mGal")
        self.paxes.ticklabel_format(useOffset=False)

        self.cal = self.paxes.plot([], [], zorder=10, color='blue')
        self.obs = self.paxes.plot([], [], '.', zorder=1, color='orange')

        self.axes = fig.add_subplot(212)
        self.axes.xaxis.set_label_text(self.xlabel)
        self.axes.yaxis.set_label_text("Altitude (m)")

        tmp = self.cbar(self.mdata)
        tmp[:, :, 3] = 0

        self.ims2 = self.axes.imshow(tmp.copy(), interpolation='nearest',
                                     aspect='auto')
        self.ims = self.axes.imshow(tmp.copy(), interpolation='nearest',
                                    aspect='auto')
        self.figure.canvas.draw()

        self.bbox = self.figure.canvas.copy_from_bbox(self.axes.bbox)
        self.pbbox = self.figure.canvas.copy_from_bbox(self.paxes.bbox)
        self.prf = self.axes.plot([0, 0])
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
        nmode = self.axes.get_navigate_mode()
        if event.button == 1:
            self.press = False
            if nmode == 'ZOOM':
                extent = self.axes.get_xbound()
                self.paxes.set_xbound(extent[0], extent[1])
                self.figure.canvas.draw()
            else:
                self.myparent.update_model()

    def move(self, event):
        """ Mouse is moving """
        if self.figure.canvas.toolbar._active is None:
            vlim = self.axes.viewLim
            dlim = self.axes.dataLim
            tmp0 = self.axes.transData.transform((vlim.x0, vlim.y0))
            tmp1 = self.axes.transData.transform((vlim.x1, vlim.y1))
            width, height = tmp1-tmp0
            width /= self.mdata.shape[1]
            height /= self.mdata.shape[0]
            width *= dlim.width/vlim.width
            height *= dlim.height/vlim.height
            cwidth = (2*self.mywidth-1)
            cb = QtGui.QBitmap(cwidth*width, cwidth*height)
            cb.fill(QtCore.Qt.color1)
            self.setCursor(QtGui.QCursor(cb))

        if event.inaxes == self.axes and self.press is True:
            row = int((event.ydata - self.lmod.zrange[0])/self.lmod.d_z)+1
            col = int((event.xdata)/self.lmod.dxy)

            aaa = self.axes.get_xbound()[-1]
            bbb = self.mdata.shape[1]
            ccc = aaa/bbb
            col = int((event.xdata)/ccc)

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

        i = xstart
        while i < xend:
            tmp = (self.crd == self.crd[i])
            tmp = np.logical_and(tmp[:, 0], tmp[:, 1])
            tmp = tmp.nonzero()[0]
            if tmp[-1] >= xend:
                xend = tmp[-1]+1
            i += 1

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

    def init_grid(self, dat, extent, dat2, opac):
        """ Updates the single color map """
        # Note that because we clear the current axes, we must put the objects
        # back into it are the graph will go blank on a draw(). This is the
        # reason for the ims and prf commands below.

        self.paxes.set_xbound(extent[0], extent[1])
        self.ims.set_visible(False)
        self.axes.set_xlim(extent[0], extent[1])
        self.axes.set_ylim(extent[2], extent[3])

        if dat2 is not None:
            self.ims2.set_data(dat2.data)
            self.ims2.set_extent(self.dat_extent(dat2))
            self.ims2.set_clim(dat2.data.min(), dat2.data.max())

        self.figure.canvas.draw()
        QtWidgets.QApplication.processEvents()
        self.bbox = self.figure.canvas.copy_from_bbox(self.axes.bbox)

        self.ims.set_visible(True)
        self.ims.set_extent(extent)
        tmp = self.luttodat(dat)
        self.ims.set_data(tmp)
        self.ims.set_alpha(opac)

        self.lbbox = self.figure.canvas.copy_from_bbox(self.axes.bbox)
        self.figure.canvas.draw()
        QtWidgets.QApplication.processEvents()

        self.mdata = dat

    def slide_grid(self, dat, dat2=None, opac=1.0):
        """ Slider """
        self.mdata = dat
        tmp = self.luttodat(dat)
        self.ims.set_data(tmp)
        self.ims.set_alpha(opac)

        self.figure.canvas.restore_region(self.bbox)
        self.axes.draw_artist(self.ims)
        self.figure.canvas.update()

        self.lbbox = self.figure.canvas.copy_from_bbox(self.axes.bbox)
        self.axes.draw_artist(self.prf[0])
        self.figure.canvas.update()

    def update_line(self, xrng, yrng):
        """ Updates the line position """
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
        return (left, right, bottom, top)

# This section is just for the profile line plot

    def extentchk(self, extent):
        """ Checks extent """
        dmin = extent[2]
        dmax = extent[3]
        if dmin == dmax:
            dmax = dmin+1
        return dmin, dmax

    def init_plot(self, xdat, dat, extent, xdat2, dat2):
        """ Updates the single color map """
        self.paxes.autoscale(False)
        dmin, dmax = self.extentchk(extent)
        self.paxes.cla()
        self.paxes.ticklabel_format(useOffset=False)
        self.paxes.set_title(self.ptitle)
        self.axes.xaxis.set_label_text(self.xlabel)
        self.paxes.yaxis.set_label_text(self.punit)
        self.paxes.set_ylim(dmin, dmax)
        self.paxes.set_xlim(extent[0], extent[1])
        self.figure.canvas.draw()
        QtWidgets.QApplication.processEvents()
        self.pbbox = self.figure.canvas.copy_from_bbox(self.paxes.bbox)

        self.paxes.set_autoscalex_on(False)
        if xdat2 is not None:
            self.obs = self.paxes.plot(xdat2, dat2, '.', zorder=1, color='orange')
        else:
            self.obs = self.paxes.plot([], [], '.', zorder=1, color='orange')
        self.cal = self.paxes.plot(xdat, dat, zorder=10, color='blue')
        self.figure.canvas.draw()
        QtWidgets.QApplication.processEvents()
        self.plotisinit = True

    def slide_plot(self, xdat, dat, xdat2, dat2):
        """ Slider """
        self.figure.canvas.restore_region(self.pbbox)
        if xdat2 is not None:
            self.obs[0].set_data([xdat2, dat2])
        else:
            self.obs[0].set_data([[], []])
        self.cal[0].set_data([xdat, dat])

        if xdat2 is not None:
            self.paxes.draw_artist(self.obs[0])
        self.paxes.draw_artist(self.cal[0])

        self.figure.canvas.update()

        QtWidgets.QApplication.processEvents()
