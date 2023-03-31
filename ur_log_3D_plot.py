from flask import Flask, render_template
import plotly.graph_objs as go
import numpy as np

app = Flask(__name__, template_folder='/path/to/index.html')





def index():
    # log_visitor_data()
    # set the set_point. The point teh robot is supposed to be 
    set_point = np.array([-0.14995162552737207, -0.5500245181144349, 0.003493531513422826, -2.191088669758009, -2.246109749965637, 0.001736848950366638])

    # read the log file
    log_file = np.loadtxt('/path/to/.log', delimiter=',') 

    # extract the x, y, z, rx, ry, rz columns from the log file
    x_values = log_file[:, 0]
    y_values = log_file[:, 1]
    z_values = log_file[:, 2]
    rx_values = log_file[:, 3]
    ry_values = log_file[:, 4]
    rz_values = log_file[:, 5]

    # calculate the Euclidean distance between the set_point and each line coordinates
    distances = np.sqrt((x_values - set_point[0])**2 + (y_values - set_point[1])**2 + (z_values - set_point[2])**2
                        + (rx_values - set_point[3])**2 + (ry_values - set_point[4])**2 + (rz_values - set_point[5])**2)

    # set the distances that are within 70-90% range to a value between 0 and 1
    min_dist = np.min(distances)
    max_dist = np.max(distances)
    yellow_range = (0.7 * max_dist) + (0.3 * min_dist)
    yellow_distances = np.where((distances >= 0.7 * max_dist) & (distances < 0.9 * max_dist),
                                (distances - yellow_range) / (0.2 * max_dist - 0.7 * max_dist), distances)

    # create the scatter plot
    scatter = go.Scatter3d(
        x=x_values,
        y=y_values,
        z=z_values,
        mode='markers',
        marker=dict(
            size=5,
            color=yellow_distances,
            colorscale='Blues',
            cmin=0.7 * max_dist,
            cmax=0.9 * max_dist
        ),
        hovertext=distances,
        hoverinfo='text'
    )

    # create the set_point marker
    set_point_marker = go.Scatter3d(
        x=[set_point[0]],
        y=[set_point[1]],
        z=[set_point[2]],
        mode='markers',
        marker=dict(
            size=150,
            color='green',
            opacity=0.2,
        ),
        name='Set Point'
    )
    # create the layout
    layout = go.Layout(
        scene=dict(
            xaxis=dict(title='X'),
            yaxis=dict(title='Y'),
            zaxis=dict(title='Z'),
            aspectmode='cube'  # add this parameter
        ),
        margin=dict(l=0, r=0, b=0, t=0),
    )

    # create the figure
    fig = go.Figure(data=[scatter, set_point_marker], layout=layout)

    # render the plotly plot in the template
    plot_div = fig.to_html(full_html=False)

    # render the template
    return render_template('index.html', plot_div=plot_div)


if __name__ == '__main__':
    app.run(debug=False, port=33000)
