import pandas as pd
from coronavirus_database import Database
import matplotlib.pyplot as plt
import matplotlib.image as img
import random


def obtain_region_data():
    database = Database()

    query, column_names = database.coronavirus_region_list(region='madrid')

    df = pd.DataFrame(query)
    df.columns = column_names

    return df


def obtain_spain_data():
    database = Database()

    query, column_names = database.coronavirus_region_list()

    df = pd.DataFrame(query)
    df.columns = column_names

    return df


def obtain_spain_data():
    database = Database()

    query, column_names = database.coronavirus_spain_list(region='madrid')

    df = pd.DataFrame(query)
    df.columns = column_names

    return df


def plot_example_1_resize(df):
    fig = plt.figure(figsize=(8, 3))

    X = df['date']
    Y = df['today_new_deaths']
    plt.plot(X, Y)

    plt.title('Line Plot')
    plt.xlabel('Dates')
    plt.ylabel('Deaths')

    plt.show()


def plot_example_2_1_subplot(df):

    X = df['date']
    Y1 = df['today_new_deaths']
    Y2 = df['today_new_confirmed']

    fig = plt.figure(figsize=(16, 6))

    ax1 = plt.subplot(1, 2, 1)
    ax1.plot(X, Y1)
    ax1.set_title('Plot 1')

    ax2 = plt.subplot(1, 2, 2)
    ax2.plot(X, Y2)
    ax2.set_title('Plot 2')

    plt.show()


def plot_example_2_2_subplot(df):

    X = df['date']
    Y1 = df['today_new_deaths']
    Y2 = df['today_new_confirmed']
    Y3 = df['today_deaths']
    Y4 = df['today_confirmed']

    fig, axes = plt.subplots(2, 2, figsize=(16, 8))

    axes[0][0].plot(X, Y1)
    axes[0][0].set_title('Plot 1')

    axes[0][1].plot(X, Y2)
    axes[0][1].set_title('Plot 2')

    axes[1][0].plot(X, Y3)
    axes[1][0].set_title('Plot 3')

    axes[1][1].plot(X, Y4)
    axes[1][1].set_title('Plot 4')

    plt.show()


def plot_example_2_3_subplot(df):
    X = df['date']
    Y1 = df['today_new_deaths']
    Y2 = df['today_new_confirmed']
    Y3 = df['today_deaths']
    Y4 = df['today_confirmed']

    fig = plt.figure(figsize=(12, 8))

    ax1 = plt.subplot2grid((6, 6), (0, 0), colspan=3, rowspan=3)
    ax1.plot(X, Y1)
    ax1.set_title('Plot 1 : (0,0)')

    ax2 = plt.subplot2grid((6, 6), (0, 3), colspan=3, rowspan=3)
    ax2.plot(X, Y2)
    ax2.set_title('Plot 2 : (0,3)')

    ax3 = plt.subplot2grid((6, 6), (3, 0), rowspan=2, colspan=2)
    ax3.plot(X, Y3)
    ax3.set_title('Plot 3 : (1,0)')

    ax4 = plt.subplot2grid((6, 6), (4, 4), rowspan=1, colspan=1)
    ax4.plot(X, Y4)
    ax4.set_title('Plot 4 : (1,3)')

    fig.tight_layout()

    plt.show()


def plot_example_3_1_annotate(df):
    X = df['region_id']
    Y1 = df['today_deaths']

    fig = plt.figure(figsize=(16, 8))

    elements = len(X)

    y_pos = list(range(1, elements + 1))

    graph = plt.bar(y_pos, Y1, color='blue')

    plt.xticks(y_pos, X)
    plt.title('Region Deaths')
    plt.xlabel('Regions')
    plt.ylabel('Deaths')

    for bar, t in zip(graph, Y1):
        plt.text(bar.get_x() + bar.get_width() / 2.0, bar.get_height(), '%.0f' % t, ha='center', va='bottom')

    plt.show()


def plot_example_3_2_annotate(df):
    X = df['date']
    Y2 = df['today_new_confirmed']

    fig = plt.figure(figsize=(8, 6))

    plt.plot(X, Y2)
    plt.title('Annotating Exponential Plot using plt.annotate()')
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')

    plt.annotate(f'{X[10]} - {Y2[10]}',
                 xy=(X[10], Y2[10]),
                 arrowprops=dict(arrowstyle='->'),
                 xytext=(X[10], Y2[10] + 1000)
                 )

    plt.annotate(f'{X[20]} - {Y2[20]}',
                 xy=(X[20], Y2[20]),
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=-.2'),
                 xytext=(X[20], Y2[20] + 1500)
                 )

    plt.annotate(f'{X[30]} - {Y2[30]}',
                 xy=(X[30], Y2[30]),
                 arrowprops=dict(arrowstyle='-|>', connectionstyle='angle,angleA=90,angleB=0'),
                 xytext=(X[30], Y2[30] + 2000)
                 )

    plt.show()


def plot_example_4_axis(df):
    X = df['date']
    Y1 = df['today_new_deaths']
    fig = plt.figure(figsize=(8, 6))

    plt.plot(X, Y1)

    plt.title('Annotating Exponential Plot using plt.annotate()')
    plt.xlabel('Date')
    plt.ylabel('Deaths')

    # removing axes from the figure
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)

    # changing color of the axes
    plt.gca().spines['left'].set_color('red')
    plt.gca().spines['bottom'].set_color('green')

    # changing axes limits
    plt.xlim(len(X)-60, len(X))
    plt.ylim(1, 500)

    plt.show()


def plot_example_5_interactive(df):
    X = df['date']
    Y1 = df['today_new_deaths']
    fig = plt.figure(figsize=(8, 6))

    plt.plot(X, Y1)

    plt.title('Annotating Exponential Plot using plt.annotate()')
    plt.xlabel('Date')
    plt.ylabel('Deaths')

    # removing axes from the figure
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)

    # changing color of the axes
    plt.gca().spines['left'].set_color('red')
    plt.gca().spines['bottom'].set_color('green')

    # changing axes limits
    plt.xlim(len(X)-60, len(X))
    plt.ylim(1, 500)

    plt.show()


def plot_example_6_group_bar(df):
    X = df['region_id']
    Y1 = df['today_deaths']
    Y2 = df['today_confirmed']

    fig = plt.figure(figsize=(10, 6))

    elements = len(X)
    x_pos_Y1 = list(range(1, elements + 1))
    x_pos_Y2 = [i + 0.4 for i in x_pos_Y1]

    graph_Y1 = plt.bar(x_pos_Y1, Y1, color='tomato', label='Deaths', width=0.4)
    graph_Y2 = plt.bar(x_pos_Y2, Y2, color='dodgerblue', label='Confirmed', width=0.4)

    plt.xticks([i + 0.2 for i in x_pos_Y1], X)
    plt.title('Coronavirus by city')
    plt.ylabel('Values')
    plt.xlabel('Cities')

    # Annotating graphs
    for summer_bar, winter_bar, ts, tw in zip(graph_Y1, graph_Y2, Y1, Y2):
        plt.text(summer_bar.get_x() + summer_bar.get_width() / 2.0, summer_bar.get_height(), '%.0f' % ts,
                 ha='center', va='bottom')
        plt.text(winter_bar.get_x() + winter_bar.get_width() / 2.0, winter_bar.get_height(), '%.0f' % tw,
                 ha='center', va='bottom')

    plt.legend()
    plt.show()


def plot_example_7_ticks(df):
    X = df['region_id']
    Y1 = df['today_deaths']
    Y2 = df['today_confirmed']

    fig = plt.figure(figsize=(10, 6))

    elements = len(X)
    x_pos_Y1 = list(range(1, elements + 1))
    x_pos_Y2 = [i + 0.4 for i in x_pos_Y1]

    graph_Y1 = plt.bar(x_pos_Y1, Y1, color='tomato', label='Deaths', width=0.4)
    graph_Y2 = plt.bar(x_pos_Y2, Y2, color='dodgerblue', label='Confirmed', width=0.4)

    plt.xticks([i + 0.2 for i in x_pos_Y1], X)
    plt.title('Coronavirus by city')
    plt.ylabel('Values')
    plt.xlabel('Cities')

    # removing axes from the figure
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)

    # Modifiying ticks
    plt.xticks([i+0.2 for i in x_pos_Y1], X, fontname='Chilanka', rotation=45, fontsize=14)

    # Annotating graphs
    for summer_bar, winter_bar, ts, tw in zip(graph_Y1, graph_Y2, Y1, Y2):
        plt.text(summer_bar.get_x() + summer_bar.get_width() / 2.0, summer_bar.get_height(), '%.0f' % ts,
                 ha='center', va='bottom')
        plt.text(winter_bar.get_x() + winter_bar.get_width() / 2.0, winter_bar.get_height(), '%.0f' % tw,
                 ha='center', va='bottom')

    plt.legend()
    plt.show()


def plot_example_8_legends(df):
    X = df['region_id']
    Y1 = df['today_deaths']
    Y2 = df['today_confirmed']

    fig = plt.figure(figsize=(10, 6))

    elements = len(X)
    x_pos_Y1 = list(range(1, elements + 1))
    x_pos_Y2 = [i + 0.4 for i in x_pos_Y1]

    graph_Y1 = plt.bar(x_pos_Y1, Y1, color='tomato', label='Deaths', width=0.4)
    graph_Y2 = plt.bar(x_pos_Y2, Y2, color='dodgerblue', label='Confirmed', width=0.4)

    plt.xticks([i + 0.2 for i in x_pos_Y1], X)
    plt.title('Coronavirus by city')
    plt.ylabel('Values')
    plt.xlabel('Cities')

    # removing axes from the figure
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)

    # Modifiying ticks
    plt.xticks([i+0.2 for i in x_pos_Y1], X, fontname='Chilanka', rotation=45, fontsize=14)

    # Annotating graphs
    for summer_bar, winter_bar, ts, tw in zip(graph_Y1, graph_Y2, Y1, Y2):
        plt.text(summer_bar.get_x() + summer_bar.get_width() / 2.0, summer_bar.get_height(), '%.0f' % ts,
                 ha='center', va='bottom')
        plt.text(winter_bar.get_x() + winter_bar.get_width() / 2.0, winter_bar.get_height(), '%.0f' % tw,
                 ha='center', va='bottom')

    # modifying legend
    plt.legend(loc='upper center', ncol=2, frameon=False)

    plt.show()


def plot_example_9_1_watermarks(df):
    X = df['region_id']
    Y1 = df['today_deaths']
    Y2 = df['today_confirmed']

    fig = plt.figure(figsize=(10, 6))

    elements = len(X)
    x_pos_Y1 = list(range(1, elements + 1))
    x_pos_Y2 = [i + 0.4 for i in x_pos_Y1]

    graph_Y1 = plt.bar(x_pos_Y1, Y1, color='tomato', label='Deaths', width=0.4)
    graph_Y2 = plt.bar(x_pos_Y2, Y2, color='dodgerblue', label='Confirmed', width=0.4)

    plt.xticks([i + 0.2 for i in x_pos_Y1], X)
    plt.title('Coronavirus by city')
    plt.ylabel('Values')
    plt.xlabel('Cities')

    # removing axes from the figure
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)

    # Text Watermark
    fig.text(0.85, 0.15, 'Coronavirus',
             fontsize=65, color='gray',
             ha='right', va='bottom', alpha=0.4, rotation=25)

    # Modifiying ticks
    plt.xticks([i+0.2 for i in x_pos_Y1], X, fontname='Chilanka', rotation=45, fontsize=14)

    # Annotating graphs
    for summer_bar, winter_bar, ts, tw in zip(graph_Y1, graph_Y2, Y1, Y2):
        plt.text(summer_bar.get_x() + summer_bar.get_width() / 2.0, summer_bar.get_height(), '%.0f' % ts,
                 ha='center', va='bottom')
        plt.text(winter_bar.get_x() + winter_bar.get_width() / 2.0, winter_bar.get_height(), '%.0f' % tw,
                 ha='center', va='bottom')

    # modifying legend
    plt.legend(loc='upper center', ncol=2, frameon=False)

    plt.show()


def plot_example_9_2_watermarks_and_save(df):
    X = df['region_id']
    Y1 = df['today_deaths']
    Y2 = df['today_confirmed']

    fig = plt.figure(figsize=(10, 6))

    elements = len(X)
    x_pos_Y1 = list(range(1, elements + 1))
    x_pos_Y2 = [i + 0.4 for i in x_pos_Y1]

    graph_Y1 = plt.bar(x_pos_Y1, Y1, color='tomato', label='Deaths', width=0.4)
    graph_Y2 = plt.bar(x_pos_Y2, Y2, color='dodgerblue', label='Confirmed', width=0.4)

    plt.xticks([i + 0.2 for i in x_pos_Y1], X)
    plt.title('Coronavirus by city')
    plt.ylabel('Values')
    plt.xlabel('Cities')

    # removing axes from the figure
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)

    # Image Watermark
    av_logo = img.imread(fname='coronavirus.jpg')
    fig.figimage(av_logo, 100, 70, alpha=0.3)

    # Modifiying ticks
    plt.xticks([i+0.2 for i in x_pos_Y1], X, fontname='Chilanka', rotation=45, fontsize=14)

    # Annotating graphs
    for summer_bar, winter_bar, ts, tw in zip(graph_Y1, graph_Y2, Y1, Y2):
        plt.text(summer_bar.get_x() + summer_bar.get_width() / 2.0, summer_bar.get_height(), '%.0f' % ts,
                 ha='center', va='bottom')
        plt.text(winter_bar.get_x() + winter_bar.get_width() / 2.0, winter_bar.get_height(), '%.0f' % tw,
                 ha='center', va='bottom')

    # modifying legend
    plt.legend(loc='upper center', ncol=2, frameon=False)

    plt.savefig(fname='corona.png')

    plt.show()



def test_function():
    fig = plt.figure(figsize=(6, 6))

    temp = [random.uniform(20, 40) for i in range(5)]
    city = ['City A', 'City B', 'City C', 'City D', 'City E']
    y_pos = list(range(1, 6))

    graph = plt.bar(y_pos, temp, color='violet')

    plt.xticks(y_pos, city)
    plt.title('City Temperature')
    plt.xlabel('Cities')
    plt.ylabel('Deaths ($^\circ$C)')

    for bar, t in zip(graph, temp):
        plt.text(bar.get_x() + bar.get_width() / 2.0, bar.get_height(), '%.2f $^\circ$C' % t, ha='center', va='bottom')

    plt.show()



if __name__ == '__main__':
    df = obtain_region_data()
    df_spain = obtain_spain_data()

    # test_function()

    # plot_example_1_resize(df)
    # plot_example_2_1_subplot(df)
    # plot_example_2_2_subplot(df)
    # plot_example_2_3_subplot(df)
    # plot_example_3_1_annotate(df_spain)
    # plot_example_3_2_annotate(df)
    # plot_example_4_axis(df)
    # plot_example_5_interactive(df)
    # plot_example_6_group_bar(df_spain)
    # plot_example_7_ticks(df_spain)
    # plot_example_8_legends(df_spain)
    # plot_example_9_1_watermarks(df_spain)
    plot_example_9_2_watermarks_and_save(df_spain)

