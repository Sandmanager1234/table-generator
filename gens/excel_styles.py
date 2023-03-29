from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font

ft_arial_white = Font(
    name='Arial',
    size = 10,
    bold= True,
    color= '00FFFFFF'
    )

ft_arial_blue = Font(
    name='Arial',
    size = 10,

    color= '000000FF'
    )

fill_black = PatternFill(
    fill_type= 'solid',
    bgColor='00000000'
)

ft_arial_black = Font(
    name = 'Arial',
    size=10
)

cats_align = Alignment(
    horizontal='center'
)

urls_align = Alignment(
    vertical='center',
    horizontal='left'
)

center_align = Alignment(
    vertical='center',
    horizontal='center',
    wrap_text=True
)

ft_calibri_black = Font(
    name='Calibri',
    size=11
)