# Fractals

Simple fractal generator

# Installation

    pip install fractals
   
# Usage

    from PIl import Image
    import fractals
    img = Image.new('RGB', (5000, 5000), (0, 0, 0))
    figures = Figures(im=img)
    figures.von_koch_curve_flake((2500, 2500), 2000,6)
    img.save("test.bmp") 
   
# Documentation

Complete documentation can be found (here)[]