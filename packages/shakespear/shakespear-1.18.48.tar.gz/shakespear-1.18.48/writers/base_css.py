from .constants import COLOR_PALETTE, DEFAULT

BASIC_CSS_CLASSES = """
        .rounded-div {{
            border-radius: 5px;
        }}

        .center-text {{
            text-align: center
        }}

        .bottom-margin {{
            margin: 0 0 10px 0
        }}

        .small-margin {{
            margin: 5px !important;
        }}

        .no-margin {{
            margin: 0px !important;
        }}
        
        table {{
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
        }}

        
        td, th {{
            border:none;
            text-align: left;
            padding: 8px;
        }}
        
        tr {{
            background-color: white;
            border-bottom: 1px solid #e5e6e6;
        }}
        
        tr:nth-child(even) {{
            background-color:  #e5e6e6 !important;
        }}
       
        h3 {{
            margin-bottom:0;
            margin-top:0;
            padding: 5px;            
        }}
        
        .table-container {{
            background-color: {lighter_grey}
            padding: 5px;
            margin-bottom: 15px;
        }}
        
        .table-header {{
            margin-top: -5px;
            margin-right: -5px;
            margin-left: -5px;
            margin-bottom: 0;
            padding: 5px;
            background-color: {dark_grey};
            color: white;
        }}
        
        .table-header-info {{
            border-bottom: 2px solid {blue};
        }}
        
        .table-header-success {{
            border-bottom: 2px solid {green};
        }}
        
        .table-header-warn {{
            border-bottom: 2px solid {yellow};
        }}
        
        .table-header-error {{
            border-bottom: 2px solid {red};
        }}
        
        .well {{
            background-color: {light_grey};
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
        }}
        
        .small-padding {{
            padding: 5px;
         }}
         
        .background-info {{
            background-color: {blue};
            border-radius: 5px;
            color: white;
        }}
         
        .background-success {{
            background-color: {green};
            border-radius: 5px;
            color: white;
        }}
         
         .background-warn {{
            background-color: {yellow};
            border-radius: 5px;
            color: white;
         }}
         
         .background-error {{
            background-color: {red};
            border-radius: 5px;
            color: white;         
         }}
""".format(
    yellow=COLOR_PALETTE.get('yellow', DEFAULT),
    green=COLOR_PALETTE.get('green', DEFAULT),
    blue=COLOR_PALETTE.get('blue', DEFAULT),
    red=COLOR_PALETTE.get('red', DEFAULT),
    light_grey=COLOR_PALETTE.get('light_grey', DEFAULT),
    dark_grey=COLOR_PALETTE.get('dark_grey', DEFAULT),
    lighter_grey=COLOR_PALETTE.get('lighter_grey', DEFAULT)
)