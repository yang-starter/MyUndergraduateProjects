import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import college


def convert_to_2d(lats, lons, values):
    latmin = 40.48
    lonmin = -74.28
    latmax = 40.93
    lonmax = -73.65
    lon_vals = np.mgrid[lonmin:lonmax:200j]
    lat_vals = np.mgrid[latmin:latmax:200j]
    map_values = np.zeros([200, 200])
    dlat = lat_vals[1] - lat_vals[0]
    dlon = lon_vals[1] - lon_vals[0]
    for lat, lon, value in zip(lats, lons, values):
        lat_idx = int(np.rint((lat - latmin) / dlat))
        lon_idx = int(np.rint((lon - lonmin) / dlon))
        if not np.isnan(value):
            map_values[lon_idx, lat_idx] = value
    return lat_vals, lon_vals, map_values


def make_plot(data_values, title='', colors='Greens'):
    lat_vals, lon_vals, values = convert_to_2d(blocks.Latitude, blocks.Longitude, data_values)
    fig = plt.figure(1, figsize=[10, 10])
    # fig.patch.set_facecolor('grey')
    limits = np.min(lon_vals), np.max(lon_vals), np.min(lat_vals), np.max(lat_vals)
    im = plt.imshow(values.T, origin='lower', cmap=colors, extent=limits)
    plt.xlabel('Longitude [degrees]')
    plt.ylabel('Latitude [degrees]')
    plt.title(title)
    plt.colorbar(im, fraction=0.025, pad=0.04)

    plt.show()


if __name__ == '__main__':
    blocks = pd.read_csv('E://census_block_loc.csv')
    census = pd.read_csv('E://nyc_census_tracts.csv', index_col=0)

    blocks = blocks[blocks.County.isin(['Bronx', 'Kings', 'New York', 'Queens', 'Richmond'])]
    blocks['Tract'] = blocks.BlockCode // 10000
    blocks = blocks.merge(census, how='left', right_index=True, left_on='Tract')

    # print(blocks.head())
    blocks.info()
    blocks.Income = pd.to_numeric(blocks.Income, errors='coerce')

    make_plot(blocks.Income, colors='Reds', title='Income')
    # make_plot(blocks.IncomePerCap, colors='inferno', title='Per Capita Income ($)')
    # blocks.to_csv('block.csv', encoding='utf-8')
    # print(blocks.Asian)

