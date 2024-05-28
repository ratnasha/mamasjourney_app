def mama():
  def load_last_period_date(file_suffix):
        try:
            data = github.read_json(f"last_period_date_{file_suffix}.json")
            last_period_date = pd.to_datetime(data["last_period_date"])
        except:
            last_period_date = None
        return last_period_date

    def save_last_period_date(date, file_suffix):
        github.write_json(f"last_period_date_{file_suffix}.json", {"last_period_date": date.strftime("%Y-%m-%d")}, "Save last period date")

    def calculate_due_date(last_period_date):
        gestation_period = timedelta(days=280)
        due_date = last_period_date + gestation_period
        return due_date

    calendar_weeks_data = {
        'Kalenderwoche': list(range(1, 41)),
        'Ereignis': ['Ultraschall', 'Arztbesuch', 'Ernährungsberatung', 'Geburtsvorbereitungskurs', 'Ruhestunde'] * 8
    } 

    st.title("mamasjourney :ship:")

    file_suffix = username
    last_period_date = load_last_period_date(file_suffix)

    st.header('Mama')
    if last_period_date is not None:
        last_period_date = st.date_input('Letzter Menstruationszyklus', value=last_period_date, format="YYYY/MM/DD")
    else:
        last_period_date = st.date_input('Letzter Menstruationszyklus', format="YYYY/MM/DD")

    if last_period_date:
        due_date = calculate_due_date(last_period_date)
        st.write("Voraussichtlicher Geburtstermin:", due_date)
        st.subheader('Schwangerschafts-Timeline')
        df_calendar_weeks = pd.DataFrame(calendar_weeks_data)
        st.write(df_calendar_weeks)

    st.write('Gewicht')
    mama_weight_date = st.date_input("Datum", value=datetime.today(), min_value=last_period_date, max_value=datetime.today(), format="YYYY/MM/DD")
    mama_weight = st.number_input("Gewicht (kg)", min_value=0.0)
    if st.button("Gewicht speichern"):
        new_row = pd.DataFrame({"Datum": [mama_weight_date], "Gewicht (kg)": [mama_weight]})
        file_name = f"mama_weights_{file_suffix}.csv"
        if github.file_exists(file_name):
            mama_weights_df = github.read_df(file_name)
            mama_weights_df = pd.concat([mama_weights_df, new_row], ignore_index=True)
        else:
            mama_weights_df = new_row.copy()
        github.write_df(file_name, mama_weights_df, "Speicher Gewicht")

    st.subheader('Gewichtsdaten')
    if github.file_exists(f"mama_weights_{file_suffix}.csv"):
        mama_weights_df = github.read_df(f"mama_weights_{file_suffix}.csv")
        st.write(mama_weights_df)
    else:
        st.write("Noch keine Gewichtsdaten vorhanden.")

    st.write('Blutwert')
    blutwerte_text = st.text_area("Blutzuckerwerte")
    if st.button("Blutwert speichern"):
        new_row = pd.DataFrame({"Datum": [mama_weight_date], "Blutzuckerwert (in mg/dL)": [blutwerte_text]})
        file_name = f"mama_blutwert_{file_suffix}.csv"
        if github.file_exists(file_name):
            mama_blutwert_df = github.read_df(file_name)
            mama_blutwert_df = pd.concat([mama_blutwert_df, new_row], ignore_index=True)
        else:
            mama_blutwert_df = new_row.copy()
        github.write_df(file_name, mama_blutwert_df, "Speicher Blutzuckerwert")

    st.subheader('Blutzuckerwert')
    if github.file_exists(f"mama_blutwert_{file_suffix}.csv"):
        mama_blutwert_df = github.read_df(f"mama_blutwert_{file_suffix}.csv")
        st.write(mama_blutwert_df)
    else:
        st.write("Noch keine Blutzuckerwerte vorhanden.")
                
    st.header('Tagebuch')
    tagebuch_text = st.text_area("Tagebuch")
    if st.button("Eintrag speichern"):
        new_row = pd.DataFrame({"Date": [mama_weight_date], "Tagebuch": [tagebuch_text]})
        file_name = f"tagebuch_{file_suffix}.csv"
        if github.file_exists(file_name):
            tagebuch_df = github.read_df(file_name)
            tagebuch_df = pd.concat([tagebuch_df, new_row], ignore_index=True)
        else:
            tagebuch_df = new_row.copy()
        github.write_df(file_name, tagebuch_df, "Speicher Tagebucheintrag")

    st.subheader('Tagebuch')
    if github.file_exists(f"tagebuch_{file_suffix}.csv"):
        tagebuch_df = github.read_df(f"tagebuch_{file_suffix}.csv")
        st.write(tagebuch_df)
    else:
        st.write("Noch keine Tagebucheinträge vorhanden.")
