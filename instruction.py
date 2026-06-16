# /// script
# dependencies = [
#     "ipyniivue==2.4.4",
#     "marimo",
# ]
# requires-python = ">=3.12"
# ///

import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from ipyniivue import NiiVue, MultiplanarType, ShowRender

    return MultiplanarType, NiiVue, ShowRender


@app.cell
def _(mo):
    eval_name=mo.ui.text(label="Please Enter Your Full Name")
    eval_name
    return


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
def _():
    return


if __name__ == "__main__":
    app.run()
