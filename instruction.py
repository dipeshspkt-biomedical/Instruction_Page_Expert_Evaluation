# /// script
# dependencies = [
#     "ipyniivue==2.4.4",
#     "marimo",
#     "pandas==3.0.3",
# ]
# requires-python = ">=3.12"
# ///

import marimo

__generated_with = "0.23.9"
app = marimo.App(width="full", layout_file="layouts/instruction.grid.json")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from ipyniivue import NiiVue, MultiplanarType, ShowRender
    import pandas as pd

    return MultiplanarType, NiiVue, ShowRender, pd


@app.cell
def _(mo):
    class Questions:
        Q1=mo.md("""
                ### With respect to overall contour quality and acceptability of the segmented hippocampus would you:\n
                1. Reject the contour, there are clear major errors and susbstantial correction is requred
                2. Request revision, there are minor but relevant errors that should be corrected
                3. Accept the contour, there are small but clinically irrelavant errors
                4. Accept the contour, it is very accurate
                """)
        Q2=mo.md("""###  With respect to omission of true hippocampal tissue, would you:\n
                1. Reject the contour; there is clear major undersegmentation
                2. Request revision; there is minor but relevant undersegmentation
                3. Accept the contour; there is slight undersegmentation, but it is not clinically relevant
                4. Accept the contour; there is no meaningful undersegmentation
                """)
        Q3=mo.md(""" ### With respect to inclusion of non-hippocampal tissue, would you:\n
                1. Reject the contour; there is clear major oversegmentation
                2. Request revision; there is minor but relevant oversegmentation
                3. Accept the contour; there is slight oversegmentation, but it is not clinically relevant
                4. Accept the contour; there is no meaningful oversegmentation  
            """)

    return (Questions,)


@app.cell
def _():
    labels=["Mask 1", "Mask 2", "Mask 3"]
    return (labels,)


@app.cell
def _(mo):
    mo.center(mo.md("# **Instruction for Evaluation of Segmentation Mask of Hippocampus Segmentation**"))
    return


@app.cell
def _(mo):
    mo.center(mo.md("## Please read the following instructions carefully"))
    return


@app.cell
def _(mo):
    eval_name=mo.ui.text(label="Please Enter Your Full Name")
    eval_name
    return


@app.cell
def _(mo):
    img_info=mo.md("**You are viewing image index:0**")
    return (img_info,)


@app.cell
def _(MultiplanarType, NiiVue, ShowRender):
    nv = NiiVue(height=800,
                    back_color=(1, 1, 1, 1),
                    show_3d_crosshair=True,
                    is_colorbar=False,
                    multiplanar_show_render=ShowRender.ALWAYS,
                    multiplanar_layout=MultiplanarType.AUTO,
                    show_bounds_border=True,
                    bounds_border_color=(1,0,0,1),
                    loading_text="Please Load Image"
                )
    nv.opts.drag_mode = "PAN"
    nv.opts.font_color=(0,1,1,1)
    nv.opts.font_size_scaling=1.5
    nv.overlay_outline_width = 0.5
    nv
    return (nv,)


@app.cell
def _(mo, nv):
    nv.load_volumes([{"url": str(mo.notebook_location()/"public"/"Input.nii.gz")},{"url": str(mo.notebook_location()/"public"/"HARP_Scratch_pred.nii.gz"),"colormap":"red"},{"url": str(mo.notebook_location()/"public"/"TUTH_Scratch_pred.nii.gz"),"colormap":"blue"},{"url": str(mo.notebook_location()/"public"/"OASIS_Scratch_pred.nii.gz"),"colormap":"green"}])
    return


@app.cell
def _(nv):
    def overlay_change(value=None):
        for i in range(1,len(nv.volumes)):
            nv.volumes[i].opacity=0
        if len(value.index.tolist())==1:
            nv.volumes[value.index.tolist()[0]+1].opacity=1

    def update_alpha(value=None):
        nv.overlay_alpha_shader=value



    return overlay_change, update_alpha


@app.cell
def _(Questions, mo, update_alpha):
    class Controls(object):
        Q1=mo.ui.array(elements=[mo.ui.dropdown(options=[1,2,3,4])]*3)
        Q2=mo.ui.array(elements=[mo.ui.dropdown(options=[1,2,3,4])]*3)
        Q3=mo.ui.array(elements=[mo.ui.dropdown(options=[1,2,3,4])]*3)


        def create_tabs(self):
            self.tabs=mo.ui.tabs({"Query 1":Questions().Q1,"Query 2":Questions().Q2,"Query 3":Questions().Q3})
            return self.tabs

        def alpha_shader(self):
            self.alpha_shader=mo.ui.slider(start=0,stop=1,step=0.1,value=1,label="Alpha Shader",on_change=update_alpha)
            return self.alpha_shader

    return (Controls,)


@app.cell
def _(Controls, labels, pd):
    Q1=Controls.Q1
    Q2=Controls.Q2
    Q3=Controls.Q3
    df=pd.DataFrame({
        "Mask":labels,
        "Query 1":Q1,
        "Query 2":Q2,
        "Query 3":Q3
    })
    return Q1, Q2, Q3, df


@app.cell
def _(Controls, df, mo, overlay_change):
    question_tabs=Controls().create_tabs()
    alpha_shader=Controls().alpha_shader()
    table=mo.ui.table(data=df,pagination=True,selection="single",label="Evaluation Form",on_change=overlay_change)
    return alpha_shader, question_tabs, table


@app.cell
def _(Q1, Q2, Q3, mo):
    submit_button=mo.ui.button(label="Submit and move to next image",disabled=any(item is None for item in Q1.value) or any(item is None for item in Q2.value ) or any(item is None for item in Q3.value))
    return (submit_button,)


@app.cell
def _(alpha_shader, img_info, mo, nv, question_tabs, submit_button, table):
    combined_widget=mo.vstack([mo.hstack([alpha_shader,img_info],widths=[1,1]),mo.hstack([nv,mo.vstack([question_tabs,table])],widths=[2,1]),submit_button])
    return (combined_widget,)


@app.cell
def _(combined_widget):
    combined_widget
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
