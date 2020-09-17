from ways import load_map_from_csv
import matplotlib.pyplot as plt

# draw graph of Heuristics time (x-axis) and Actual time (y-axis) (for question 9)

def draw_dots():
    # list of all the x
    x_list = []
    # list of all the y
    y_list = []
    with open('results/AStarRuns.txt', 'r') as file:
        for line in file:
            split_line = line.split(',')
            x_list.append(float(split_line[0]))
            y_list.append(float(split_line[1]))

    plt.axis([-0.01, 0.2, -0.01, 0.2])
    # Draw a point at the desirable location
    plt.scatter(x_list, y_list, s=10)
    # Set chart title.
    plt.title("AStar Results", fontsize=19)
    # Set x axis label.
    plt.xlabel("Heuristics time", fontsize=10)
    # Set y axis label.
    plt.ylabel("Actual time", fontsize=10)
    # Display the plot in the matplotlib's viewer.
    plt.show()

draw_dots()
