# # # # # # # # # # # # # # # # # # # # # # # # # #
# Plotting class based on MatPlotLib (PyLab)
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import os

import matplotlib

# does not need $DISPLAY - must be called before import pylab
matplotlib.use ('Agg')

import numpy
import scipy
import pylab
import pandas
import re
#import suftware

# # warnings management
# import warnings
# warnings.filterwarnings ("ignore", message="No labelled objects found. ")
# warnings.filterwarnings(
#     "ignore",
#     message="elementwise comparison failed; returning scalar instead,\
#              but in the future will perform elementwise comparison",
# )

# figure configuration
matplotlib.rcParams ["figure.max_open_warning"] = 100
matplotlib.rcParams ["savefig.dpi"] = 300

# font configuration
matplotlib.rcParams ["font.size"] = 16
matplotlib.rcParams ["legend.fontsize"] = 14
# matplotlib.rcParams ['lines.linewidth']       = 3
# matplotlib.rcParams ['lines.markeredgewidth'] = 3
# matplotlib.rcParams ['lines.markersize']      = 10

# additional colors
matplotlib.colors.ColorConverter.colors ["spux_blue"] = (38 / 256.0, 135 / 256.0, 203 / 256.0)
matplotlib.colors.ColorConverter.colors ["spux_orange"] = (251 / 256.0, 124 / 256.0, 42 / 256.0)
matplotlib.colors.ColorConverter.colors ["spux_green"] = (182 / 256.0, 212 / 256.0, 43 / 256.0)

# large colorlist for unified color selection in plots
colorlist = [ color for index, color in matplotlib.colors.cnames.items () ]
colorlist = sorted (colorlist)
rng = numpy.random.RandomState (seed=1)
rng.shuffle (colorlist)

# === helper routines

# create a new solid color which is slighly brighter
def brighten(color, factor=0.7):

    if color is None:
        return None
    rgb = list(matplotlib.colors.ColorConverter().to_rgb(color))
    brighter = rgb
    for channel, value in enumerate(rgb):
        brighter[channel] += factor * (1.0 - value)
    return tuple(brighter)

# generate figure name using the format 'figpath/pwd_suffix.extension'
def figname(save, figpath="fig", suffix="", extension="pdf"):

    if save is not None:
        return save

    if not os.path.exists(figpath):
        os.mkdir(figpath)
    runpath, rundir = os.path.split(os.getcwd())
    if suffix == "":
        return os.path.join(figpath, rundir + "_" + "." + extension)
    else:
        return os.path.join(figpath, rundir + "_" + suffix + "." + extension)

# filter to remove special characters from strings to be used as filenames
def plain (name):
    return re.sub (r'\W+', '', name)

# color presets for some specific plots
colors = {}
colors["evaluate"] = "lightgray"

colors["init"] = "green"
colors["init sync"] = "lightgreen"

colors["run"] = "spux_orange"
colors["observe"] = "goldenrod"
colors["likelihoods"] = "chocolate"
colors["run sync"] = "sandybrown"

colors["routings"] = "darkturquoise"
colors["resample"] = "steelblue"
colors["route"] = "teal"
colors["replicate"] = "mediumorchid"
colors["resample sync"] = "lightskyblue"

colors["bcast parameters"] = "g"
colors["scatter particles"] = "b"
colors["bcast time"] = "c"
colors["scatter routings"] = "r"
colors["wait"] = "y"
colors["gather likelihoods"] = "m"

# classiffication of certain performance indicators as communication
communications = [
    "bcast parameters",
    "scatter particles",
    "bcast time",
    "scatter routings",
    "route",
    "wait",
    "gather likelihoods",
]

# preset order of the legend entries
order = []
order += ["evaluate"]
order += ["bcast parameters"]
order += ["scatter particles"]
order += ["init"]
order += ["init sync"]
order += ["bcast time"]
order += ["routings"]
order += ["scatter routings"]
order += ["wait"]
order += ["resample"]
order += ["route"]
order += ["replicate"]
order += ["resample sync"]
order += ["run"]
order += ["observe"]
order += ["likelihoods"]
order += ["run sync"]
order += ["gather likelihoods"]

class MatPlotLib (object):

    # constructor
    def __init__ (self, samples=[], infos=[], prior=None, title=0, autosave=1):
        
        print (' :: Initializing MatPlotLib plotter...')

        self.samples = samples
        self.infos = infos
        self.prior = prior
        self.title = title
        self.autosave = autosave
        self.chains = len (infos [0] ['likelihoods']) if infos is not None and len (infos) > 0 else None
        self.labels = list (prior.labels if prior is not None else self.samples.columns.values)
        self.indices = numpy.arange (len (samples) // self.chains) if self.chains is not None else []

    # plot line and range and return handles for legend
    def line_and_range(
        self,
        xs,
        lower,
        middle,
        upper,
        color="k",
        alpha=0.6,
        style="-",
        linewidth=1,
        marker=None,
        logx=0,
        logy=0,
    ):

        pylab.fill_between(
            xs,
            lower,
            upper,
            facecolor=brighten(color),
            edgecolor=brighten(color),
            alpha=alpha,
            linewidth=0,
        )
        area, = pylab.plot([], [], color=brighten(color), alpha=alpha, linewidth=10)

        line, = pylab.plot(
            xs,
            middle,
            style,
            color=color,
            linewidth=linewidth,
            marker=marker,
            markersize=10,
            markeredgewidth=linewidth,
        )

        if logx:
            pylab.xscale("log")
        if logy:
            pylab.yscale("log")

        return (area, line)

    # save figure
    def save(self, save, formats=["eps", "png", "pdf", "svg"]):

        if isinstance(formats, list):
            base_name = save[:-4]
            for format in formats:
                pylab.savefig(base_name + "." + format, bbox_inches="tight")
        else:
            pylab.savefig(save, bbox_inches="tight")

    # show figures
    def show(self):

        pylab.show()
    
    # compute extents
    def extents (self, x, y, alpha=0.99):

        xv = self.samples [x]
        yv = self.samples [y]

        # get prior support intervals, if available
        intervals = self.prior.intervals (alpha) if self.prior is not None else None

        # compute plotting extents
        xvmin = xv.min ()
        xvmax = xv.max ()
        yvmin = yv.min ()
        yvmax = yv.max ()
        xpmin = intervals [x] [0] if intervals is not None else xvmin
        xpmax = intervals [x] [1] if intervals is not None else xvmax
        ypmin = intervals [y] [0] if intervals is not None else yvmin
        ypmax = intervals [y] [1] if intervals is not None else yvmax
        xmin = min (xpmin, xvmin)
        xmax = max (xpmax, xvmax)
        ymin = min (ypmin, yvmin)
        ymax = max (ypmax, yvmax)

        return xmin, xmax, ymin, ymax
    
    # plot dataset
    def datasets (self, datasets, legend=True, save=None, suffix='', color=None, scientific=0, frame=0):
        
        for label in list (datasets.values ()) [0] .columns.values:

            if not frame:
                print (' :: Plotting datasets for %s' % label)
                pylab.figure()
            names = sorted (list (datasets.keys ()))
            for index, name in enumerate (names):
                data = datasets [name]
                ylabel = label
                xlabel = data.index.name
                if color is None:
                    datacolor = colorlist [index]
                else:
                    datacolor = color
                observations, = pylab.plot (
                    data.index, data [ylabel],
                    marker="o",
                    markeredgecolor=datacolor, markerfacecolor='none',
                    markersize=6, markeredgewidth=2, linewidth=0,
                    label="observation " + str (name)
                    )
            if not frame:
                pylab.ylabel (ylabel)
                pylab.xlabel (xlabel)
            if self.title:
                pylab.title ("obseravations (data)")
            if legend:
                pylab.legend (loc='best')
            
            if scientific:
                pylab.gca().ticklabel_format (axis='both', style='sci', scilimits=(-2, 2))

            if not frame:
                pylab.draw()
                self.save(figname(save, suffix="datasets-%s%s" % (plain (ylabel), suffix)))
            else:
                return observations

    # plot marginal distributions of all parameters
    def distributions (self, distribution, color='spux_blue', alpha=0.99, columns=3, samples=None, title=False, save=None, suffix=''):
        
        plots = len (distribution.labels)
        rows = numpy.ceil (plots / columns)
        pylab.figure (figsize = (8 * columns, 5 * rows))
        
        intervals = distribution.intervals (alpha)
        for index, label in enumerate (sorted (distribution.labels)):
            print (' :: Plotting distribution for %s...' % label)
            pylab.subplot (rows, columns, index + 1)
            interval = list (intervals [label])
            extent = interval [1] - interval [0]
            interval [0] -= 0.2 * extent
            interval [1] += 0.2 * extent
            x = numpy.linspace (interval [0], interval [1], 1000)
            pylab.plot (x, distribution.mpdf (label, x), color=color, linestyle='-', lw=5)
            ylim = list (pylab.ylim ())
            ylim [0] = 0
            ylim [1] *= 1.05
            pylab.ylim (ylim)
            if samples is not None:
                for name, sample in samples.items ():
                    pylab.axvline (sample [label], color='r', linestyle='--', lw=5, label=name)
            pylab.ylim (ylim)
            pylab.xlabel (label)
            pylab.ylabel ('pdf of %s' % label)
            if self.title:
                pylab.title("prior")
            pylab.draw()
        self.save(figname(save, suffix="distributions%s" % suffix))
    
    # plot marginal distributions over the prediction values extent in the datasets
    def errors (self, error, datasets, parameters, percentiles, color='spux_green', columns=3, scientific=0, title=False, save=None, suffix=''):
        
        data_labels = list (datasets.values ()) [0] .columns.values
        plots = len (data_labels)
        rows = numpy.ceil (plots / columns)
        
        for name, dataset in datasets.items ():

            print (" :: Plotting errors for dataset ", name)
            
            pylab.figure (figsize = (8 * columns, 5 * rows))

            for index, label in enumerate (data_labels):

                pylab.subplot (rows, columns, index + 1)
                
                predictions = dataset [label] .dropna ()

                upper = numpy.empty (len (predictions.index))
                middle = numpy.empty (len (predictions.index))
                lower = numpy.empty (len (predictions.index))

                for ti, time in enumerate (predictions.index):
                    
                    distribution = error.distribution (dataset.loc [time], parameters)
                    lower [ti], upper [ti] = distribution.intervals (1 - 2 * percentiles [label] / 100.0) [label]
                
                    if hasattr (error, 'transform'):
                        middle [ti] = error.transform (dataset.loc [time], parameters) [label]
                    else:
                        middle [ti] = predictions.loc [time]
                
                percentiles_handle = self.line_and_range (predictions.index, lower, middle, upper, linewidth=2, color=color, alpha=0.9)
                single_dataset = { name : pandas.DataFrame (middle, columns=[label], index=predictions.index) }
                observations_handle = self.datasets (single_dataset, save, suffix, color='dimgray', frame=1)
                pylab.ylabel (('transformed ' if hasattr (error, 'transform') else '') + label)
                pylab.xlabel (dataset.index.name)
                handles = [percentiles_handle, observations_handle]
                labels = ["error (%s - %s percentiles)" % (str(percentiles [label]), str(100 - percentiles [label])), "observations"]
                if scientific:
                    pylab.gca().ticklabel_format (axis='both', style='sci', scilimits=(-2, 2))
                pylab.legend (handles, labels, loc="best")

            if self.title:
                pylab.title ("errors")
            pylab.draw ()
            self.save(figname(save, suffix="errors-dataset-%s%s" % (name, suffix)))

    # evaluate 1D kde estimator
    def kde (self, samples, x):

        # density = suftware.DensityEstimator (samples)
        # return density.evaluate (x)

        density = scipy.stats.gaussian_kde (samples)
        return density (x)
    
    # plot marginal posterior distributions of all parameters
    def posteriors (self, initial=True, MAP=None, alpha=0.99, columns=3, exact=None, prior=True, legend=False, save=None, suffix=''):

        plots = len (self.prior.labels)
        rows = numpy.ceil (plots / columns)
        pylab.figure (figsize = (8 * columns, 5 * rows))
        
        intervals = self.prior.intervals (alpha)
        for index, label in enumerate (sorted (self.prior.labels)):
            pylab.subplot (rows, columns, index + 1)
            interval = list (intervals [label])
            extent = interval [1] - interval [0]
            interval [0] -= 0.2 * extent
            interval [1] += 0.2 * extent
            x = numpy.linspace (interval [0], interval [1], 1000)
            if prior:
                pylab.plot (x, self.prior.mpdf (label, x), color='spux_blue', linestyle='-', lw=5)
            pylab.plot (x, self.kde (self.samples [label] .values, x), color='spux_orange', linestyle='-', lw=5)
            ylim = list (pylab.ylim ())
            ylim [0] = 0
            ylim [1] *= 1.05
            pylab.ylim (ylim)
            if MAP is not None:
                pylab.axvline (MAP [label], color='k', linestyle='--', lw=5)
            if exact is not None:
                pylab.axvline (exact [label], color='r', linestyle='--', lw=5)
            pylab.ylim (ylim)
            pylab.xlabel (label)
            pylab.ylabel ('pdf of %s' % label)
            if self.title:
                pylab.title("posterior")
            pylab.draw()
        self.save(figname(save, suffix="posteriors%s" % suffix))

    # compute pairwise joint kde
    def kde2d (self, xv, yv, xmin, xmax, ymin, ymax, points=100j):

        # estimate posterior PDF with a KDE
        xsg, ysg = numpy.mgrid[xmin:xmax:points, ymin:ymax:points]
        positions = numpy.vstack([xsg.ravel(), ysg.ravel()])
        values = numpy.vstack([xv, yv])
        kernel = scipy.stats.gaussian_kde(values)
        Z = numpy.reshape(kernel(positions).T, xsg.shape)
        return Z
    
    # return maximum a posteriori (MAP) estimate of parameters and the associated likelihood
    def MAP (self):

        MAP_parameters = None
        MAP_likelihood = float ('-inf')
        MAP_infos = None
        for info in self.infos:
            for chain in range (len (info ['likelihoods'])):
                if info ['likelihoods'] [chain] > MAP_likelihood:
                    MAP_likelihood = info ['likelihoods'] [chain]
                    MAP_parameters = info ['parameters'] .loc [chain]
                    MAP_infos = info ['infos'] [chain]
        return MAP_parameters, MAP_likelihood, MAP_infos
    
    # plot pairise joint posteriors matrix
    def posteriors2d_matrix (self, initial=True, MAP=None, exact=None, legend=False, save=None, suffix=''):
        pylab.figure ()
        pandas.plotting.scatter_matrix (self.samples, alpha=0.2, figsize=(6, 6), diagonal='kde')
        self.save(figname(save, suffix="posteriors2d-matrix" + suffix))
    
    # plot pairwise joint posteriors of all parameters
    # TODO: make a matrix of this plot,
    # with chains in subdiagonals, and hexbin (see pandas.plotting) in superdiagonalas
    def posteriors2d (self, initial=True, MAP=None, exact=None, legend=False, save=None, suffix=''):

        for i, label_i in enumerate (sorted (self.labels)):
            for j, label_j in enumerate (sorted (self.labels) [i + 1:]):
                self.posterior2d (label_i, label_j, initial, MAP, exact, legend, save, suffix)

    # plot pairwise joint posterior
    # TODO: add burnin cutoff, chains toggle, and hexbin option - see pandas plotting
    def posterior2d (self, x, y, initial=True, MAP=None, exact=None, legend=False, save=None, suffix=""):
        
        print (' :: Plotting joint posterior for %s and %s (%d chains)' % (x, y, self.chains))

        xv = self.samples[x]
        yv = self.samples[y]

        xmin, xmax, ymin, ymax = self.extents (x, y)
        
        pylab.figure()

        # plot 2d KDE for posterior PDF
        kde2d = self.kde2d (xv, yv, xmin, xmax, ymin, ymax)
        pylab.imshow(
            numpy.transpose (kde2d),
            origin="lower",
            aspect="auto",
            extent=[xmin, xmax, ymin, ymax],
            cmap="YlOrBr",
        )
        colorbar = pylab.colorbar()
        colorbar.set_label("probability density")

        # plot all posterior samples and paths of each chain
        for chain in range (self.chains):
            pylab.plot (xv [chain::self.chains], yv[chain::self.chains], color=colorlist [chain], marker=".", markersize=10, markeredgewidth=0, alpha=0.5, label="chain %d" % chain)
        pylab.xlim([xmin, xmax])
        pylab.ylim([ymin, ymax])

        # plot initial parameter set
        if initial:
            x0 = self.samples [x][0:self.chains]
            y0 = self.samples [y][0:self.chains]
            pylab.plot (x0, y0, marker="+", color="olivedrab", markersize=14, markeredgewidth=3, linewidth=0)
            # TODO: add a _single_ label entry for 'initial' marker
        
        # plot MAP
        if MAP is not None:
            pylab.plot (MAP [x], MAP [y], marker="o", color="k", markerfacecolor='none', markersize=10, markeredgewidth=2, linewidth=0, label="MAP")

        # plot exact parameter set
        if exact is not None:
            pylab.plot (exact[x], exact[y], marker="x", color="r", markersize=10, markeredgewidth=3, linewidth=0, label="exact")
        
        # add legend
        if legend:
            pylab.legend (loc="best", numpoints=1)

        if self.title:
            pylab.title("joint posterior")
        pylab.xlabel(x)
        pylab.ylabel(y)
        pylab.draw()
        self.save(figname(save, suffix="posterior2d-%s-%s%s" % (plain (x), plain (y), suffix)))

    # plot likelihoods (and acceptances, if provided)
    def likelihoods (self, save=None, suffix="", start=1):
        
        print (' :: Plotting likelihoods and acceptances')

        pylab.figure()
        
        # likelihoods
        for chain in range (self.chains):
            likelihood = [ info ['likelihoods'] [chain] + info ['priors'] [chain] for info in self.infos ]
            variance = numpy.empty (len (self.infos))
            if 'variance' in self.infos [0] ['infos'] [0]:
                for index, info in enumerate (self.infos):
                    try:
                        variance [index] = info ['infos'] [chain] ['variance']
                    except:
                        variance [index] = float ('nan')
            else:
                for index, info in enumerate (self.infos):
                    try:
                        variances = [ replicate ['variance'] for replicate in info ['infos'] [chain] ['infos'] .values () ]
                        variance [index] = numpy.sum (variances)
                    except:
                        variance [index] = float ('nan')
            lower = likelihood - numpy.sqrt (variance)
            upper = likelihood + numpy.sqrt (variance)
            handles_likelihood = self.line_and_range (self.indices, lower, likelihood, upper, linewidth=2, color="darkmagenta")
        pylab.xlabel("sample")
        pylab.ylabel("log-prior + log-likelihood")

        # acceptances
        acceptances = 'accepts' in self.infos [0]
        if acceptances:
            pylab.sca (pylab.twinx())
            for chain in range (self.chains):
                accept = [ info ['accepts'] [chain] for info in self.infos ]
                rolling = numpy.cumsum (accept [start:]) / numpy.arange (1, len (accept) + 1 - start, dtype=float)
                handles_accept, = pylab.plot (self.indices [start:], rolling, color="forestgreen", linewidth=2, zorder=-1)
            pylab.ylabel("acceptance rate")
            pylab.ylim((-0.05, 1.05))

        handles_likelihood = handles_likelihood [::-1]
        labels = ["estimate", "error"]
        if acceptances:
            handles_likelihood += (handles_accept,)
            labels += ["acceptance rate"]
        pylab.legend (handles_likelihood, labels, loc="best")

        pylab.xlim((self.indices[0], self.indices[-1]))
        if self.title:
            pylab.title ("log-likelihood" + (" and acceptance rate" if acceptances else ""))
        pylab.draw()
        self.save(figname(save, suffix="likelihoods" + suffix))
    
    # plot autocorrelations
    def autocorrelations (self, save=None, suffix='', split=1):
        
        for label, series in self.samples.iteritems ():
            print (' :: Plotting autocorrelations for %s (%d chains)' % (label, self.chains))
            pylab.figure ()
            if split:
                for chain in range (self.chains):
                    pandas.plotting.autocorrelation_plot (series [chain::self.chains], lw=2, color=colorlist [chain])
            else:
                pandas.plotting.autocorrelation_plot (series, lw=5, color='r')
            self.save(figname(save, suffix="autocorrelations-%s" % plain (label) + suffix))

    # plot posterior model predictions including observations
    # plot a color-coded kde for each time, instead of just a mean and spread
    def predictions (self, datasets, MAP_infos=None, percentile=25, mode='posterior', scientific=0, columns=3, save=None, suffix=""):
        
        if 'predictions' in self.infos [0] ['infos'] [0]:
            print (' :: ERROR: prediction plotting implemented only for replicates')
            return
        
        plots = len (datasets)
        rows = numpy.ceil (plots / columns)
        
        for label in list (datasets.values ()) [0] .columns.values:

            pylab.figure (figsize = (8 * columns, 5 * rows))

            for plot, (name, dataset) in enumerate (datasets.items ()):
                
                print (' :: Plotting predictions for', label)
                times = list (dataset.index)
                lower = numpy.empty (len (times))
                upper = numpy.empty (len (times))

                for index, time in enumerate (times):
                    values = []
                    for info in self.infos:
                        try:
                            values += [ value [label] for chain in info ['infos'] for value in chain ['infos'] [name] ['predictions'] [mode] [time] ]
                        except:
                            pass
                    lower [index] = numpy.percentile (values, percentile)
                    upper [index] = numpy.percentile (values, 100 - percentile)
                
                # find the prediction among particles with the largest observational likelihood within the MAP
                MAP_values = numpy.empty (len (times))
                for index, time in enumerate (times):
                    PF_infos = MAP_infos ['infos'] [name]
                    MAP_values [index] = None
                    MAP_error = float ('-inf')
                    for particle, error in enumerate (PF_infos ['errors'] [time]):
                        if error > MAP_error:
                            MAP_error = error
                            MAP_values [index] = PF_infos ['predictions'] [mode] [time] [particle] [label]

                pylab.subplot (rows, columns, plot + 1)
                predictions = self.line_and_range (times, lower, MAP_values, upper, "spux_orange", alpha=0.6, style="-", linewidth=2)
                observations = self.datasets ({ name : dataset [[label]] }, save, suffix, color='dimgray', frame=1)
                pylab.ylabel (label)
                pylab.xlabel (dataset.index.name)
                if self.title:
                    pylab.title (mode + " model predictions and dataset " + name)
                pylab.legend ([predictions, observations], [mode + " predictions (%s - %s percentiles)" % (str(percentile), str(100-percentile)), "observations"], loc="best")
                if scientific:
                    pylab.gca().ticklabel_format (axis='both', style='sci', scilimits=(-2, 2))
                pylab.draw()
            
            self.save (figname (save, suffix="predictions-%s-%s%s" % (mode, plain (label), suffix)))
    
    # === TODO: all routines below need recheck due to modified 'infos' structure in the code
    
    # # plot redraw rate
    # def redraw(self, save=None, suffix=""):

    #     pylab.figure()
    #     means = [numpy.mean(list(info["redraw"].values())) for info in self.infos]
    #     lower = [numpy.min(list(info["redraw"].values())) for info in self.infos]
    #     upper = [numpy.max(list(info["redraw"].values())) for info in self.infos]

    #     handles = self.line_and_range(
    #         self.indices, lower, means, upper, color="olivedrab"
    #     )
    #     pylab.legend(handles, ["range", "mean"], loc="best")

    #     if self.title:
    #         pylab.title("particle redraw rate")
    #     pylab.xlabel("sample")
    #     pylab.xlim((self.indices[0], self.indices[-1]))
    #     pylab.ylabel("redraw rate")
    #     pylab.ylim([-0.05, 1.05])
    #     pylab.legend(loc="best")
    #     pylab.draw()
    #     self.save(figname(save, suffix="redraw" + suffix))

    # # plot traffic
    # def traffic(self, keys=["move", "copy"], save=None, suffix=""):

    #     if not isinstance(keys, list):
    #         keys = ["init", "move", "cost", "copy", "kill"]
    #     pylab.figure()
    #     colors = dict(
    #         zip(
    #             ["init", "move", "cost", "copy", "kill"],
    #             ["g", "spux_orange", "magenta", "spux_blue", "k"],
    #         )
    #     )
    #     handles = []
    #     for key in keys:
    #         color = colors[key]
    #         means = [
    #             numpy.mean(
    #                 [measurement[key] for time, measurement in info["traffic"].items()]
    #             )
    #             for info in self.infos
    #         ]
    #         lower = [
    #             numpy.min(
    #                 [measurement[key] for time, measurement in info["traffic"].items()]
    #             )
    #             for info in self.infos
    #         ]
    #         upper = [
    #             numpy.max(
    #                 [measurement[key] for time, measurement in info["traffic"].items()]
    #             )
    #             for info in self.infos
    #         ]
    #         handles.append(
    #             self.line_and_range(self.indices, lower, means, upper, color=color)
    #         )
    #     pylab.legend(handles, keys, loc="best")
    #     if self.title:
    #         pylab.title("traffic fractions")
    #     pylab.xlabel("sample")
    #     pylab.xlim((self.indices[0], self.indices[-1]))
    #     pylab.ylabel("traffic [fraction]")
    #     pylab.ylim([-0.05, 1.05])
    #     pylab.legend(loc="best")
    #     pylab.draw()
    #     self.save(figname(save, suffix="traffic" + suffix))

    # # plot runtimes
    # def runtimes(
    #     self,
    #     keys=[
    #         "init",
    #         "init sync",
    #         "run",
    #         "run sync",
    #         "route",
    #         "replicate",
    #         "resample sync",
    #     ],
    #     legendpos="",
    #     save=None,
    #     suffix="",
    # ):

    #     if not isinstance(keys, list):
    #         keys = list(self.infos[0]["runtimes"].keys())

    #     keys = [key for key in order if key in keys]

    #     pylab.figure()
    #     handles = []
    #     for key in keys:
    #         color = colors[key]
    #         style = ":" if (key in communications or "sync" in key) else "-"
    #         scalar = 0 if isinstance(self.infos[0]["runtimes"][key], list) else 1
    #         if scalar:
    #             means = [info["runtimes"][key] for info in self.infos]
    #             handles += pylab.plot(self.indices, means, style, color=color)
    #         else:
    #             means = [numpy.mean(info["runtimes"][key]) for info in self.infos]
    #             # lower = [ numpy.min (info ['runtimes'] [key]) for info in self.infos ]
    #             # upper = [ numpy.max (info ['runtimes'] [key]) for info in self.infos ]
    #             lower = [
    #                 numpy.percentile(info["runtimes"][key], 10) for info in self.infos
    #             ]
    #             upper = [
    #                 numpy.percentile(info["runtimes"][key], 90) for info in self.infos
    #             ]
    #             handles.append(
    #                 self.line_and_range(
    #                     self.indices, lower, means, upper, color=color, style=style
    #                 )
    #             )
    #     if len(keys) <= 7:
    #         pylab.legend(handles, keys, loc="best")
    #     else:
    #         pylab.legend(handles, keys, loc="center left", bbox_to_anchor=(1, 0.5))
    #     if self.title:
    #         pylab.title("runtimes")
    #     pylab.xlabel("sample")
    #     pylab.xlim((self.indices[0], self.indices[-1]))
    #     pylab.ylabel("runtime [s]")
    #     pylab.draw()
    #     self.save(figname(save, suffix="runtimes" + suffix))

    # # plot efficiency: (init + run + replicate + observe + likelihood) / evaluate
    # # TODO: plot spread of efficiencies over all ensembles
    # def efficiency(self, save=None, suffix=""):

    #     evaluate = numpy.array([info["runtimes"]["evaluate"] for info in self.infos])
    #     init = numpy.array(
    #         [numpy.mean(info["runtimes"]["init"]) for info in self.infos]
    #     )
    #     replicate = numpy.array(
    #         [numpy.mean(info["runtimes"]["replicate"]) for info in self.infos]
    #     )
    #     run = numpy.array([numpy.mean(info["runtimes"]["run"]) for info in self.infos])
    #     observe = numpy.array(
    #         [numpy.mean(info["runtimes"]["observe"]) for info in self.infos]
    #     )
    #     likelihoods = numpy.array(
    #         [numpy.mean(info["runtimes"]["likelihoods"]) for info in self.infos]
    #     )
    #     efficiencies = (init + replicate + run + observe + likelihoods) / evaluate

    #     pylab.figure()
    #     pylab.plot(self.indices, efficiencies, color="saddlebrown")
    #     if self.title:
    #         pylab.title("parallelization efficiencies")
    #     pylab.xlabel("sample")
    #     pylab.xlim((self.indices[0], self.indices[-1]))
    #     pylab.ylabel("parallelization efficiency")
    #     pylab.ylim([-0.05, 1.05])
    #     pylab.legend(loc="best")
    #     pylab.draw()
    #     self.save(figname(save, suffix="efficiencies" + suffix))

    # # plot timestamps
    # def timestamps(
    #     self,
    #     keys=[
    #         "routings",
    #         "wait",
    #         "init",
    #         "init sync",
    #         "resample",
    #         "resample sync",
    #         "run",
    #         "run sync",
    #     ],
    #     sample=0,
    #     limit=10,
    #     save=None,
    #     suffix="",
    # ):

    #     if not isinstance(keys, list):
    #         keys = list(self.infos[sample]["timestamps"].keys())
    #     start = self.infos[sample]["timestamps"]["evaluate"][0][0]
    #     final = self.infos[sample]["timestamps"]["evaluate"][0][1]

    #     keys = [key for key in order if key in keys]

    #     offset = lambda timestamp: (timestamp[0] - start, timestamp[1] - start)
    #     linewidth = 0.6
    #     patch = lambda timestamp, level: (
    #         (timestamp[0], level - 0.5 * linewidth),
    #         timestamp[1] - timestamp[0],
    #         linewidth,
    #     )

    #     pylab.figure()
    #     handles = {}
    #     for key in keys:
    #         color = colors[key]
    #         # style = '-' if (key in communications or 'sync' in key) else '-'
    #         alpha = 0.5 if (key in communications or "sync" in key) else 1.0
    #         master = (
    #             0 if isinstance(self.infos[sample]["timestamps"][key][0], list) else 1
    #         )
    #         if master:
    #             for timestamp in self.infos[sample]["timestamps"][key]:
    #                 xy, w, h = patch(offset(timestamp), 0)
    #                 pylab.gca().add_patch(
    #                     pylab.Rectangle(xy, w, h, color=color, alpha=alpha, linewidth=0)
    #                 )
    #                 handles[key], = pylab.plot(
    #                     [], [], color=color, alpha=alpha, linewidth=10
    #                 )
    #                 # handles [key], = pylab.plot (offset (timestamp), (limit, limit),
    #                 # style, color=color, linewidth = linewidth, alpha = alpha)
    #         else:
    #             total = min(limit, len(self.infos[sample]["timestamps"][key]))
    #             for worker, timestamps in enumerate(
    #                 self.infos[sample]["timestamps"][key]
    #             ):
    #                 if limit is not None and worker == limit:
    #                     break
    #                 for timestamp in timestamps:
    #                     xy, w, h = patch(offset(timestamp), worker + 1)
    #                     pylab.gca().add_patch(
    #                         pylab.Rectangle(
    #                             xy, w, h, color=color, alpha=alpha, linewidth=0
    #                         )
    #                     )
    #                     handles[key], = pylab.plot(
    #                         [], [], color=color, alpha=alpha, linewidth=10
    #                     )
    #                     # handles [key], = pylab.plot (offset (timestamp), (worker,
    #                     # worker), style, color = color, linewidth = linewidth,
    #                     # alpha = alpha)
    #     pylab.legend(
    #         [handles[key] for key in keys],
    #         keys,
    #         loc="center left",
    #         bbox_to_anchor=(1, 0.5),
    #     )
    #     if self.title:
    #         pylab.title("timestamps")
    #     pylab.xlabel("time [s]")
    #     pylab.ylabel("worker")
    #     pylab.xlim((0, final - start))
    #     pylab.ylim((-0.5, total + 0.5))
    #     if total <= 20:
    #         pylab.yticks(
    #             range(total + 1), ["M "] + ["%3d " % worker for worker in range(total)]
    #         )
    #     pylab.gca().invert_yaxis()
    #     pylab.setp(pylab.gca().get_yticklines(), visible=False)
    #     pylab.draw()
    #     self.save(figname(save, suffix=("timestamps-S%05d" % sample) + suffix))

    # # plot scaling and average efficiencies from multiple simulations
    # def scaling(self, workerslist, infosdict, factors={}, save=None, suffix=""):

    #     evaluate = {}
    #     init = {}
    #     replicate = {}
    #     run = {}
    #     observe = {}
    #     likelihoods = {}
    #     efficiencies = {}

    #     for workers, infos in infosdict.items():

    #         evaluate[workers] = numpy.array(
    #             [info["runtimes"]["evaluate"] for info in infos]
    #         )
    #         init[workers] = numpy.array(
    #             [numpy.mean(info["runtimes"]["init"]) for info in infos]
    #         )
    #         replicate[workers] = numpy.array(
    #             [numpy.mean(info["runtimes"]["replicate"]) for info in infos]
    #         )
    #         run[workers] = numpy.array(
    #             [numpy.mean(info["runtimes"]["run"]) for info in infos]
    #         )
    #         observe[workers] = numpy.array(
    #             [numpy.mean(info["runtimes"]["observe"]) for info in infos]
    #         )
    #         likelihoods[workers] = numpy.array(
    #             [numpy.mean(info["runtimes"]["likelihoods"]) for info in infos]
    #         )
    #         efficiencies[workers] = (
    #             init[workers]
    #             + replicate[workers]
    #             + run[workers]
    #             + observe[workers]
    #             + likelihoods[workers]
    #         ) / evaluate[workers]

    #     # apply scaling factors if needed
    #     if factors != {}:
    #         for workers, runtime in evaluate.items():
    #             runtime *= factors[workers]

    #     pylab.figure()

    #     # scaling
    #     means = [numpy.mean(evaluate[workers]) for workers in workerslist]
    #     lower = [numpy.percentile(evaluate[workers], 10) for workers in workerslist]
    #     upper = [numpy.percentile(evaluate[workers], 90) for workers in workerslist]
    #     linear, = pylab.plot(
    #         workerslist,
    #         [means[0] * workerslist[0] / workers for workers in workerslist],
    #         "--",
    #         color="forestgreen",
    #         linewidth=3,
    #         alpha=0.5,
    #     )
    #     runtime = self.line_and_range(
    #         workerslist,
    #         lower,
    #         means,
    #         upper,
    #         color="forestgreen",
    #         marker="+",
    #         linewidth=3,
    #         logx=1,
    #         logy=1,
    #     )
    #     pylab.ylabel("runtime [s]")
    #     pylab.ylim(0.5 * pylab.ylim()[0], 2 * pylab.ylim()[1])
    #     pylab.xlabel("number of workers")

    #     # efficiencies
    #     pylab.sca(pylab.twinx())
    #     means = [numpy.mean(efficiencies[workers]) for workers in workerslist]
    #     lower = [numpy.percentile(efficiencies[workers], 10) for workers in workerslist]
    #     upper = [numpy.percentile(efficiencies[workers], 90) for workers in workerslist]
    #     efficiency = self.line_and_range(
    #         workerslist,
    #         lower,
    #         means,
    #         upper,
    #         color="saddlebrown",
    #         marker="+",
    #         linewidth=3,
    #         logx=1,
    #     )
    #     pylab.ylabel("efficiency")
    #     pylab.ylim([-0.05, 1.05])

    #     pylab.xlim(0.5 * pylab.xlim()[0], 2 * pylab.xlim()[1])
    #     if self.title:
    #         pylab.title("parallel scaling and efficiency")
    #     pylab.legend(
    #         [runtime, linear, efficiency],
    #         ["runtime", "linear scaling", "efficiency"],
    #         loc="best",
    #     )
    #     pylab.draw()
    #     self.save(figname(save, suffix="scaling" + suffix))
