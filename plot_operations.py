"""
This module contains the PlotOperations class,
which contains functions for generating boxplots
and lineplots based on user-supplied weather data.
"""

import matplotlib.pyplot as plt

class PlotOperations:
    """ This class contains functions for generating boxplot and lineplot graphs for weather data supplied by the user. """
    def create_boxplot(self, weather_data, start_year, end_year):
        """Creates a box plot of the supplied weather data within the supplied date range."""
        monthly_temperatures = [[] for _ in range(12)]

        for date, data in weather_data.items():
            year = int(date.split('-')[0])
            month = int(date.split('-')[1])

            if start_year <= year <= end_year:
                monthly_temperatures[month - 1].append(data['Mean'])

        plt.boxplot(monthly_temperatures)
        plt.xlabel('Months')
        plt.ylabel('Temperature')
        plt.title(f'Boxplot of Mean Temperatures for {start_year} to {end_year}')
        plt.xticks(ticks=range(1, 13), labels=[
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ])
        plt.show()


    def create_lineplot(self, weather_data, year, month):
        """Creates a line plot of the supplied weather data from a supplied year and month."""
        temperatures = []
        for date, data in weather_data.items():
            if date.startswith(f'{year:04d}-{month:02d}'):
                temperatures.append(data['Mean'])

        days = list(range(1, len(temperatures) + 1))
        plt.figure(figsize=(12, 6))
        plt.plot(days, temperatures, marker='o')
        plt.xlabel('Day of the Month')
        plt.ylabel('Avg Daily Temp')
        plt.title('Daily Avg Temperatures')
        plt.xticks(days, [f'{year:04d}-{month:02d}-{day:02d}' for day in range(1, len(temperatures) + 1)], rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.show()
