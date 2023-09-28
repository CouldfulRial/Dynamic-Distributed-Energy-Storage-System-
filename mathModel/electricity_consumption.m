
% Time points (15 mins per sample, so 4 samples per hour)
times = [0, 4*4, 7.5*4, 11.5*4, 19*4, 24*4]; % Given time points

% Corresponding consumption values
values = 0.1 * [5.8, 5.2, 6.5, 5.7, 7.5, 5.8];

pp = spline(times, values);

% Interpolate using cubic spline
consumption = interp1(times, values, t, 'pchip');

coes = pp.coefs