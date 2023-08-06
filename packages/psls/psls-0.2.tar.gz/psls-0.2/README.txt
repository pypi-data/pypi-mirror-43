PSLS: the PLATO Solar-like Light-curve Simulator

Simulate solar-like oscillators representative for PLATO observations.
The simulator includes stochastically-excited oscillations, granulation and activity background components, as well as instrumental sources of noise representative for PLATO. The program also manages the existence of a time shift between groups of telescope.
Planetary transits are included following Mandel & Agol (2002) equations (see http://adsabs.harvard.edu/abs/2002ApJ...580L.171M) and using the Python implementation by Ian Crossfield (http://www.astro.ucla.edu/~ianc/>) at UCLA.

Two different types of oscillation spectrum can be simulated depending of the type of star:
* Redgiant stars: oscillation spectra based on the Universal Pattern (gen_up) together with the mixed modes patterns derived from the asymptotic theory ;
* Main-sequence and subgiant stars: oscillation spectra based on a set of eigenfrequencies computed with ADIPLS pulsation code.

Rotationnal mode splitings are implemented in a simplified manner.

To install the program in your home directory for you own use, type:
   python setup.py install --home=${HOME}

Edit the configuration file, an example is given in psls.yaml

Finally, execute PSLS:
	 psls.py psls.yaml

To make the code working with ADIPLS, you will also need to have a grid of stellar models. We provide two grids (credit: Takafumi Sonoi):
*  m+0y27h: stellar models with masses ranging between 0.75 and 1.15 with an initial Helium abundance Y_0=0.27 ; microscopic diffusion (no radiative accelerations) was included using the simplified equations from Michaud & Proffitt (1993). Overshoot is not included and the mixing-length parameter is fixed to 1.9
*  m+0y24h: stellar models with masses ranging between 1.20 and 2.00 with an Helium abundance Y=0.24 ; diffusion was not included as this depletes heavy elements from the upper layers of the star, due to the neglect of radiative accelerations. An overshoot of 0.2 is assumed and the mixing-length parameter is fixed to 1.6.

Note that, for RGB and clump stars, the program relies on the Universal Pattern, accordingly  stellar models are  not required for those stars.  


Copyright (c) 2014, October 2017, Reza Samadi, LESIA - Observatoire de Paris

This is a free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
 
This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with this code.  If not, see <http://www.gnu.org/licenses/>.

