import streamlit as st


def header_dashboard():
    logo = "https://i.ibb.co/6RkVJMk8/logo7.png"
    st.markdown(
        f"""
        <div style="display : flex; flex-direction : column; align-items:center; justify-content:center; margin-bottom:30px; margin-top:30px;">
               <img src='{logo}' style= 'height:120px;border-radius:20px;'>
               <h1 style ="text-align:center;color:white;margin:15px 0 0 0;
                                        padding:0;
                                        line-height:1;
                                        letter-spacing:2px;">
                                         <div style="letter-spacing:8px;">
                                            SENTIN
                                        </div>
                                        <div style="letter-spacing:0px;">
                                            AI
                                        </div>
                                    </div>""",
         unsafe_allow_html=True
     
    )

def kpi_cards():
        st.markdown("""
                <style>
        
                
        
                .st-key-metric_cards [data-testid="stMetric"] {
                    background: #ffffff;
                    border: 1px solid #e1e5ea;
                    border-radius: 12px;
                    padding: 20px 10px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        
                    display: flex !important;
                    flex-direction: column !important;
                    align-items: center !important;
                    justify-content: center !important;
                    text-align: center !important;
                    transition: width 0.5s ease, height 0.5s ease!important
                }

                .st-key-metric_cards [data-testid="stMetric"]:hover{
                         transform: scale(1.05)
                         
                }
        
        
                /* LABEL CENTER*/
        
                .st-key-metric_cards [data-testid="stMetricLabel"] {
                    width: 100% !important;
        
                    display: flex !important;
                    align-items: center !important;
                    justify-content: center !important;
        
                    text-align: center !important;
                }
        
        
                /* Streamlit ka nested label div */
                .st-key-metric_cards [data-testid="stMetricLabel"] > div {
                    width: 100% !important;
        
                    display: flex !important;
                    align-items: center !important;
                    justify-content: center !important;
        
                    text-align: center !important;
                }
        
        
                /* Actual label text */
                .st-key-metric_cards [data-testid="stMetricLabel"] p {
                    width: 100% !important;
                    text-align: center !important;
                    justify-content: center !important;
                    margin: 0 !important;
                }
        
        
                /*  VALUE CENTER  */
        
                .st-key-metric_cards [data-testid="stMetricValue"] {
                    width: 100% !important;
                    text-align: center !important;
                }
        
        
                .st-key-metric_cards [data-testid="stMetricValue"] > div {
                    width: 100% !important;
                    text-align: center !important;
                }
        
        
                /* Equal card gap */
                .st-key-metric_cards [data-testid="stHorizontalBlock"] {
                    gap: 16px;
                }
        
                </style>
                """, unsafe_allow_html=True)
    
def Fonts_styling():
   
      st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Archivo+Black&family=Black+Ops+One&family=Jockey+One&family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&family=Open+Sans:ital,wght@0,300..800;1,300..800&family=Outfit:wght@100..900&display=swap');
              h1{
             font-family : "Black Ops One" , sans-serif !important;
             font-size : 4.5rem !important;
             line-height : 1rem important;
             margin-bottom : 0rem !important
             } 
              h2{
                 font-family : "Alfa Slab One" , sans-serif !important;
                             font-size : 2.5rem !important;
                             font-weight : 700!important
                             line-height : 0.8 !important;
                             margin-bottom : 0rem !important;
                             display: flex !important;
                             justify-content: center !important;
                             align-items: center !important;     
             
                              } 
              h3,h4{
                          font-family : "Outfit" , sans-serif !important;
                          
                          font-weight : 700!important;
                          font-size : 1.5rem !important;
                         line-height : 0.8 !important;
                        margin-bottom : 0rem !important;
                          display: flex !important;
                        justify-content: center !important; 
                        align-items: center !important;     
                        }  
             


                .live-status {
                            font-family: "Outfit", sans-serif !important;
                            font-size: 1.05rem !important;
                            font-weight: 600 !important;
                            color: #86EFAC !important;

                            background-color: #25312D;
                            border: 1px solid #3F6655;
                            border-radius: 8px;

                            padding: 8px 14px;
                            display: inline-block;
                            }




                    p{
                          font-family : "Outfit" , sans-serif !important;
                          
                          font-weight : 700!important;
                          font-size : 1.2rem !important;
                         line-height : 0.8 !important;
                        margin-bottom : 0rem !important;
                          display: flex !important;
                        justify-content: center !important; 
                        align-items: center !important;     
                          
                       }
                 
    

   
        </style>
         """, 
         unsafe_allow_html=True)


def background():
      st.markdown("""
            <style>


/*hiding streamlit top bar     */   
header {visibility: hidden;}
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }    
       
/* Streamlit native chart container */
[data-testid="stVegaLiteChart"],
[data-testid="stArrowVegaLiteChart"] {
    background-color: #000000!important;
    border: 1px solid #4A525B !important;
    border-radius: 12px !important;
   
}

/* Chart ke andar ka SVG */
[data-testid="stVegaLiteChart"] svg,
[data-testid="stArrowVegaLiteChart"] svg {
    background-color: #22333b !important;
    border-radius: 10px !important;
}

/* Canvas based rendering ho to */
[data-testid="stVegaLiteChart"] canvas,
[data-testid="stArrowVegaLiteChart"] canvas {
    background-color: #22333b !important;
    border-radius: 10px !important;
}


        

 [data-testid="stMarkdownContainer"]{
height:50px!important;
margin-top:10px!important;
margin-bottom:0px!important;
        }
        

 .stApp { background: linear-gradient(
        135deg,
        #30343f 50%,
        #001219 50%
    );
}
[data-testid="stAppViewContainer"] {
    background: transparent;
}

/* Normal text */
.stApp {
    color: #e5e5e5;
}

/* Heading */
h1, h2, h3,h4,h5,text{
    color: #ffffff !important;
}



#    STREAMLIT DATAFRAME FOR TABLES


[data-testid="stDataFrame"] {
    background-color: #343B43 !important;
    border: 1px solid #4A525B !important;
    border-radius: 12px !important;
    padding: 8px !important;
    overflow: hidden !important;
}

/* Dataframe ke internal wrappers */
[data-testid="stDataFrame"] > div {
    background-color: #343B43 !important;
}

/* Toolbar area */
[data-testid="stDataFrame"] [data-testid="stElementToolbar"] {
    background-color: #343B43 !important;
}

/* Static Streamlit table */
[data-testid="stTable"] {
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* Table cells */
[data-testid="stTable"] td {
    background-color: #343B43 !important;
    color: #F1F5F9 !important;
    border-color: #4A525B !important;
}

/* Table header */
[data-testid="stTable"] th {
    background-color: #414A54 !important;
    color: white !important;
    border-color: #4A525B !important;
    font-weight: 600 !important;
}


</style>
""", unsafe_allow_html=True)

def require_review_styling():
     st.markdown("""
<style>

/* 
   REVIEW CARD
 */

[class*="st-key-review_card_"] {

    max-width: 850px !important;
    width: 78% !important;

    margin-left: auto !important;
    margin-right: auto !important;

    background: #343A46 !important;

    border: 1px solid #505866 !important;
    border-radius: 14px !important;

    padding: 20px 24px !important;

    box-sizing: border-box !important;
}


/* andar ki spacing kam */
[class*="st-key-review_card_"]
[data-testid="stVerticalBlock"] {

    gap: 0.6rem !important;
}


/* 
   METRIC TEXT CENTER
 */

[class*="st-key-review_card_"]
[data-testid="stMetric"] {

    text-align: center !important;
}


[class*="st-key-review_card_"]
[data-testid="stMetricLabel"] {

    justify-content: center !important;
}


[class*="st-key-review_card_"]
[data-testid="stMetricLabel"] p {

    width: 100% !important;
    text-align: center !important;
}


[class*="st-key-review_card_"]
[data-testid="stMetricValue"] {

    width: 100% !important;
    text-align: center !important;
}


/* 
   BUTTON WRAPPER SMALLER
 */

[class*="st-key-review_card_"]
[data-testid="stButton"] {
    height:100%!important;
    width: 80% !important;

    margin-left: auto !important;
    margin-right: auto !important;
}


/* actual button */
[class*="st-key-review_card_"]
[data-testid="stButton"] > button {

    width: 100% !important;

    min-height: 70px !important;
    height: 40px !important;

    padding: 5px 14px !important;

    border-radius: 8px !important;

    font-size: 0.88rem !important;
    font-weight: 700 !important;
}


/* 
   FRAUD BUTTON
 */

[class*="st-key-fraud_"] button {

    background: #D63C3C !important;

    color: white !important;

    border: 1px solid #EC5A5A !important;
}


[class*="st-key-fraud_"] button p {

    color: white !important;
}


/* 
   LEGITIMATE BUTTON
 */

[class*="st-key-legitimate_"] button {

    background: #278E59 !important;

    color: white !important;

    border: 1px solid #3DB875 !important;
}


[class*="st-key-legitimate_"] button p {

    color: white !important;
}


/* hover */
[class*="st-key-fraud_"] button:hover {

    background: #EA4949 !important;
}


[class*="st-key-legitimate_"] button:hover {

    background: #30A768 !important;
}

</style>

""", unsafe_allow_html=True)
      






          
