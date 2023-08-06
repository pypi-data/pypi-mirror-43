CornPy: Cornell Ecology Programs in Python
******************************************
 
**CornPy** provides Python wrappers for two classic programs for ecological data analyses, DECORANA (DEtrended COrrespondence ANAlysis) and TWINSPAN (Two-Way SPecies INdicator ANalysis). Both programs were written by M. O. Hill in FORTRAN for mainframe computers, and modified for the IBM PC. 

These modified versions use the "strict" convergence criteria of Oksanen & Minchin (1997) for eigenanalysis, with a tolerance of 0.000005 and a maximum iteration limit of 999. In DECORANA, the bug in non-linear scaling has been corrected.

Besides binary executables compiled with GNU gfortran to run under MS-Windows or GNU/Linux, FORTRAN source files, decorana.f and twinspan.f, are also provided for those who wish to change the maximum dimensions (by simply changing the numbers in the first PARAMETER statement in each program). 

Both programs require an input data file in Cornell Condensed format, containing the community data to be analysed. The layout of this file should follow the same rules as for the original versions of DECORANA and TWINSPAN. The write_cep() function included in this package will automatically convert a pandas dataframe into a the required format for input to each program.

Install via 'pip install cornpy'

License
=====
**CornPy** is distributed under the GNU General Public License

Version
=====
0.1.0

Examples
======
Detrended correspondence analysis:

	import pandas as pd
    import cornpy as cp
    df = pd.read_csv("data.csv")
    site_scores, species_scores = cp.decorana(df)

Two-way species indicator analysis:

    import pandas as pd
    import cornpy as cp
    df = pd.read_csv("data.csv")
    output = twinspan(df)