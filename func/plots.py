import pandas as pd
from matplotlib.figure import Figure


def clearAxes(fig: Figure):
    """Clear axes

    :param fig:
    :return:
    """
    axs = fig.axes
    for ax in axs:
        ax.cla()


def drawGrid(fig: Figure):
    """Draw grids

    :param fig:
    :return:
    """
    axs = fig.axes
    for ax in axs:
        ax.grid(which='major', linestyle='solid')
        ax.grid(which='minor', linestyle='dotted')


def getMajorXTicks(df: pd.DataFrame) -> tuple:
    date_str = str(df.index[0].date())
    tick_labels = [
        '9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00',
        '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30',
    ]
    tick_position = [pd.to_datetime('%s %s' % (date_str, l)) for l in tick_labels]

    return tick_position, tick_labels


def getMajorXTicks2(df: pd.DataFrame) -> tuple:
    date_str = str(df.index[0].date())
    tick_labels = [
        '9:00', '9:15', '9:30', '9:45',
        '10:00', '10:15', '10:30', '10:45',
        '11:00', '11:15', '11:30', '11:45',
        '12:00', '12:15', '12:30', '12:45',
        '13:00', '13:15', '13:30', '13:45',
        '14:00', '14:15', '14:30', '14:45',
        '15:00', '15:15', '15:30'
    ]
    tick_position = [pd.to_datetime('%s %s' % (date_str, l)) for l in tick_labels]

    return tick_position, tick_labels


def refreshDraw(fig: Figure):
    fig.canvas.draw()
