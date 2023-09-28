% Generate time values (from 0 to 24*4, at steps of 1)
t = 0:1:24*4;

% Get consumption values for each time point
consumption_values = electricity_consumption(t);

% Plot
figure;
plot(t/4, consumption_values); % Convert t to hours for x-axis
xlabel('Time (hours)');
ylabel('Electricity Consumption');
title('Electricity Consumption over a Day');
grid on;
xlim([0 24]);
xticks(0:2:24); % Show every 2 hours for clarity
