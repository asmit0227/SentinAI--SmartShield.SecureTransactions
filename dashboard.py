import requests
import pandas as pd
import streamlit as st
from UI.style import header_dashboard,kpi_cards,Fonts_styling,background,require_review_styling

app_base_url="http://127.0.0.1:8000"

st.set_page_config(
    page_title="SentinAI - Smart Shield.Secure Transactions ",
    page_icon="https://i.ibb.co/6RkVJMk8/logo7.png",
    layout="wide"
)
 
#api helper
def get_api(endpoint):
   try: 
    response=requests.get(
        f"{app_base_url}{endpoint}",
        
        timeout=5
    )

    response.raise_for_status()

    return response.json()
   except requests.exceptions.RequestException as error:
     st.error(f"API connection error : {error}")
     return None
   
def post_api(endpoint, payload):
    try:
        response = requests.post(
            f"{app_base_url}{endpoint}",
            json=payload,
            timeout=5
        )

        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        st.error(f"API request failed: {error}")
        return None


@st.fragment(run_every="5s")
def live_dashboard():
    header_dashboard()
    Fonts_styling()
    background()
    require_review_styling()
    
    
    


    st.divider()

    # APIcalls

    all_information = get_api("/analytics/summary")
    transactions = get_api("/transactions?limit=100")
    fraud_alerts = get_api("/fraud/alerts?limit=20")
    review_queue = get_api("/review/queue?limit=20")
    fraud_alert_reviewed=get_api("/fraud/alert/review?limit=50")
    if not all_information:
        st.error("Dashboard data unavailable")
        return


    #Summary Values 

    total = all_information.get("total_transactions",all_information.get("total_transaction", 0))

    fraud = all_information.get("fraud_transactions",all_information.get("total_fraud_transaction", 0))

    genuine = all_information.get("genuine_transactions", all_information.get("genuine_transaction", 0))

    fraud_probability = all_information.get("average_fraud_probability", 0)

    fraud_rate = all_information.get("fraud_rate_percent", 0)



    st.markdown(
    """
    <div class="live-status">
        🟢 Live monitoring active
    </div>
    """,
    unsafe_allow_html=True
)


    #KPI Cards
    kpi_cards()

    with st.container(key="metric_cards"):
      col1, col2, col3, col4, col5 = st.columns(5)
   

      with col1:
        st.metric(
        "💳 Total Transactions",
        total,width="stretch"
      )
      with col2:
       st.metric(
        "🚨 Fraud Transactions",
        fraud,width="stretch"
      )
      with col3:
       st.metric(
        "✅ Genuine Transactions",
        genuine,width="stretch"
      )
      with col4:
         st.metric(
        "📊 Avg Fraud Probability",
        f"{fraud_probability * 100:.2f}%",width="stretch"
      )
      with col5:
         st.metric(
        "📈 Fraud Rate",
        f"{fraud_rate:.2f}%",width="stretch"
      )


    #Charts

    st.divider()
    st.subheader("📊 Transaction Analytics",text_alignment="center")
    st.divider()

    if transactions:

      chart_df = pd.DataFrame(transactions)

    col1, col2 = st.columns(2)


  
    # 1. Genuine vs Fraud
    with st.container():

      with col1:
        
        st.markdown("#### Transaction Classification",text_alignment="center")

        if "label" in chart_df.columns:

            label_counts = (
                chart_df["label"]
                .fillna("unknown")
                .str.title()
                .value_counts()
            )

            st.bar_chart(label_counts,color="#E8EDF2")


   
    # 2. Risk Distribution
  
      with col2:

         st.markdown("#### Risk Distribution",text_alignment="center")

         if "risk_level" in chart_df.columns:

            risk_counts = (
                chart_df["risk_level"]
                .fillna("unknown")
                .str.title()
                .value_counts()
            )

            st.bar_chart(risk_counts,color="#E8EDF2")

    st.divider()     

   
    # 3. Fraud Probability Trend
   
    st.markdown("#### Fraud Probability Trend",text_alignment="center")

    if (
        "fraud_probability" in chart_df.columns
        and "created_at" in chart_df.columns
    ):

        trend_df = chart_df[
            [
                "created_at",
                "fraud_probability"
            ]
        ].copy()

        trend_df["created_at"] = pd.to_datetime(
            trend_df["created_at"],
            errors="coerce"
        )

        trend_df["fraud_probability"] = (
            trend_df["fraud_probability"] * 100
        )

        trend_df = (
            trend_df
            .dropna()
            .sort_values("created_at")
            .tail(30)
        )

        trend_df = trend_df.rename(
            columns={
                "fraud_probability":
                "Fraud Probability (%)"
            }
        )

        trend_df = trend_df.set_index(
            "created_at"
        )

        st.line_chart(
            trend_df["Fraud Probability (%)"],color="#E8EDF2"
        )

    else:

     st.info("No transaction data available for analytics.")


    # 

    st.divider()
  

    st.divider()
    st.subheader("🚨 Fraud Transactions Alert",text_alignment="center")
 
    if fraud_alerts:

       fraud_alert_df = pd.DataFrame(fraud_alerts)

       fraud_columns = [
        "external_transaction_id",
        "card_id",
        "amount",
        "fraud_probability",
        "velocity_count",
        "risk_level",
        "risk_reason",
        "decision",
        "created_at"
        ]

       available_columns = [
        column
        for column in fraud_columns
        if column in fraud_alert_df.columns
    ]

       fraud_display_df = (
        fraud_alert_df[available_columns]
        .copy()
       )


    # Probability → percentage
       if "fraud_probability" in fraud_display_df.columns:
        fraud_display_df["fraud_probability"] = (
            fraud_display_df["fraud_probability"] * 100
        ).round(4)


    # Make risk readable
       if "risk_level" in fraud_display_df.columns:
        fraud_display_df["risk_level"] = (
            fraud_display_df["risk_level"]
            .fillna("N/A")
            .str.title()
        )


    # Make decision readable
       if "decision" in fraud_display_df.columns:
        fraud_display_df["decision"] = (
            fraud_display_df["decision"]
            .fillna("N/A")
            .str.title()
        )


    # Clean date format
       if "created_at" in fraud_display_df.columns:

        fraud_display_df["created_at"] = pd.to_datetime(
            fraud_display_df["created_at"],
            errors="coerce"
        )

        fraud_display_df["created_at"] = (
            fraud_display_df["created_at"]
            .dt.strftime("%d-%m-%Y %H:%M:%S")
        )


    # Friendly column names
        fraud_display_df = fraud_display_df.rename(
           columns={
            "external_transaction_id": "Transaction ID",
            "card_id": "Card ID",
            "amount": "Amount",
            "fraud_probability": "Fraud Probability (%)",
            "velocity_count": "Velocity",
            "risk_level": "Risk Level",
            "risk_reason": "Risk Reason",
            "decision": "Decision",
            "created_at": "Created At"
            }
         )
        styled_df = fraud_display_df.head(50).style.set_properties(**{
        "background-color": "#22333b",
         "color": "#F1F5F9"
})

 



        st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )

    else:
        st.info("No Fraud Alerts Found")


    # MANUAL REVIEW QUEUE


    st.subheader(
    "🕵️ Transactions Requiring Review",
    text_alignment="center"
)

    review_queue = get_api("/review/queue?limit=20")


    with st.container(key="review_queue"):

     if review_queue:

        for review_transaction in review_queue:

             transaction_id = review_transaction["transaction_id"]

             external_id = review_transaction.get(
            "external_transaction_id",
            transaction_id
        )

        fraud_probability = (
            review_transaction.get("fraud_probability", 0) * 100
        )

        with st.container(border=True,key=f"review_card_{transaction_id}"):

            
          
            st.write(
                 "Card ID :  "
                 f"{review_transaction.get('card_id', 'N/A')}"
            )    

            st.write(
                "Transaction ID : "
                 f"{review_transaction.get('transaction_id', 'N/A')}"
            )
                
            st.write(
                "Amount : "
                f"{review_transaction.get('amount', 0)}"
            )

            st.write(
                "Velocity : "
                f"{review_transaction.get('velocity_count', 0)}"
            )

            st.write(
                "Risk Level : "
                f"{review_transaction.get('risk_level', 'N/A')}"
            )

            st.write(
                "Risk Reason : "
                f"{review_transaction.get('risk_reason')}"
            )

            st.write(
                "Fraud Probability : "
                f"{review_transaction.get('fraud_probability'):.4f}%"
            )

            


            btn1, btn2 = st.columns(2)

            with btn1:

                if st.button(
                    "🚨 Confirm Fraud",
                    key=f"fraud_{transaction_id}",
                    use_container_width=True
                ):
                    result = post_api(
                        f"/review/{transaction_id}",
                        {
                            "verdict": "confirmed_fraud"
                        }
                    )

                    if result:
                        st.toast(
                            "Transaction confirmed as fraud."
                        )
                        st.rerun()


            with btn2:

                if st.button(
                    "✅ Mark Legitimate",
                    key=f"legitimate_{transaction_id}",
                    use_container_width=True
                ):

                    result = post_api(
                        f"/review/{transaction_id}",
                        {
                            "verdict": "legitimate"
                        }
                    )

                    if result:
                        st.toast(
                            "Transaction marked as reviewed."
                        )
                        st.rerun()
     else: 
       st.info(
        "No transactions currently require manual review."
         )

    st.divider()
    st.subheader("Recent Transactions",text_alignment="center")

    if transactions:

     transactions_df = pd.DataFrame(transactions)
     filtered_df = transactions_df.copy()



    # Columns that we want to show
     recent_columns = [
        "external_transaction_id",
        "card_id",
        "amount",
        "label",
        "fraud_probability",
        "velocity_count",
        "risk_level",
        "decision",
        "created_at"
    ]

     # Only keep columns that actually exist
     available_columns = [column for column in recent_columns if column in filtered_df.columns ]

     display_df = filtered_df[available_columns].head(20).copy()



    # Make fraud probability easier to read
     if "fraud_probability" in display_df.columns:
        display_df["fraud_probability"] = (
            display_df["fraud_probability"] * 100
        ).round(4)
     if "risk_level" in display_df.columns:
        display_df["risk_level"] = (
        display_df["risk_level"]
        .fillna("N/A")
        .str.title()
    )

     if "decision" in display_df.columns:
        display_df["decision"] = (
        display_df["decision"]
        .fillna("N/A")
        .str.title()
    )  
        
     if "created_at" in display_df.columns:

        display_df["created_at"] = pd.to_datetime(
        display_df["created_at"],
        errors="coerce"
    )

        display_df["created_at"] = (
        display_df["created_at"]
        .dt.strftime("%d-%m-%Y %H:%M:%S")
    )    


     # Better column names for UI
     display_df = display_df.rename(
        columns={
            "external_transaction_id": "Transaction ID",
            "card_id": "Card ID",
            "amount": "Amount",
            "label": "Prediction",
            "fraud_probability": "Fraud Probability (%)",
            "velocity_count": "Velocity",
            "risk_level": "Risk Level",
            "decision": "Decision",
            "created_at": "Created At"
        })

     styled_df_fraud = display_df.head(20).style.set_properties(**{
                "background-color": "#22333b",
                 "color": "#F1F5F9"})
    


     st.dataframe(
        styled_df_fraud,
        use_container_width=True,
        hide_index=True
    )

    else:
     st.info("No Transactions Found")


    #  Fraud Alerts Table

    st.divider()
    st.subheader("🚨 Review Transactions",text_alignment="center")

    if fraud_alert_reviewed:

        fraud_alert_df = pd.DataFrame(fraud_alert_reviewed)
        styled_df_alert = fraud_alert_df.head(20).style.set_properties(**{
                "background-color": "#22333b",
                 "color": "#F1F5F9"})

        st.dataframe(
            styled_df_alert,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No Fraud Transactions Found")

live_dashboard()        
