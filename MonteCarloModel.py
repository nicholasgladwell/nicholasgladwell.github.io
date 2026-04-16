def generate_plot():
    import numpy as np
    import plotly.graph_objects as go

    sims = 10000
    MIC = 0.5
    target = 400

    doses = [800, 1200, 1600, 2000, 2400]

    bins = np.linspace(0, 1500, 50)

    fig = go.Figure()

    pta_values = []

    for i, dose in enumerate(doses):
        Cl = np.random.lognormal(mean=np.log(5), sigma=0.4, size=sims)
        AUC = dose / Cl
        index = AUC / MIC

        hist, bin_edges = np.histogram(index, bins=bins, density=True)

        pta = (index >= target).mean()
        pta_values.append(pta)

        fig.add_trace(go.Bar(
            x=bin_edges[:-1],
            y=hist,
            visible=(i == 0),
            name=f"Dose {dose}"
        ))

    steps = []
    for i, dose in enumerate(doses):
        step = dict(
            method="update",
            args=[
                {"visible": [j == i for j in range(len(doses))]},
                {"title.text": f"Dose = {dose} | PTA = {pta_values[i]*100:.2f}%"}
            ],
            label=f'Dose: {dose} mg'
        )
        steps.append(step)

    fig.add_shape(
        type="line",
        x0=target, x1=target,
        y0=0, y1=1,
        xref="x", yref="paper",
        line=dict(dash="dash")
    )

    fig.update_layout(
        sliders=[dict(active=0, steps=steps)],
        title=f"Dose = {doses[0]} | PTA = {pta_values[0]*100:.2f}%",
        xaxis_title="AUC/MIC",
        yaxis_title="Probability Density",
        xaxis=dict(range=[0, 1500]),
        yaxis=dict(range=[0, 0.0035]) 
    )

    return fig