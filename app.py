import os
import requests
import streamlit as st
import pandas as pd
from PIL import Image
from groq import Groq
import json
import csv
from db import Database

menu = str

#fungsi tabel pada menu home
def tabel_data_jadwal():
    if os.path.exists("jadwal.csv"):    
        return pd.read_csv("jadwal.csv")
    else:
        return pd.DataFrame(columns=["ID", "Tanggal", "Jam", "Mata Kuliah", "Lokasi"])

def simpan_jadwal(df):
    df.to_csv("jadwal.csv", index=False)
    
def tabel_data_tugas():
    if os.path.exists("tugas.csv"):
        return pd.read_csv("tugas.csv")
    else:
        return pd.DataFrame(columns=["ID", "Deadline", "Nama tugas","Keterangan"])

def simpan_tugas(df):
    df.to_csv("tugas.csv", index=False)

jadwal_df = tabel_data_jadwal()
tugas_df = tabel_data_tugas()

#tampilan UI Menu sampai dengan sidebar 

st.title("SIDAC")
st.markdown("### SI Daily Activity Campus")
st.markdown("---")

menu = st.sidebar.selectbox("Pilihan Menu", ['Home', 'Hitung Nilai Akhir', 'Kalkulator', 'Kelola Matkul', 'Kelola Tugas', 'Tools AI SIDAC','Tools Todo-list'])

st.sidebar.image("myapp.jpg", width=180)
st.sidebar.title("Tentang saya")
st.sidebar.write("""Saya adalah seorang mahasiswa universitas bakrie yang sedang mengerjakan tugas project praktikum object Oriented programming 
                     yang dibimbing oleh asisten dosen bang bambang, disini saya membuat aplikasi web dengan menggunakan streamlit python secara 
                     dasarnya saja. kali ini saya membuat aplikasi SIDAC""")
with st.sidebar.expander("Author"):
    st.write(""" Created By Faiz Fathoni - 1222002005 Universitas Bakrie Sistem Informasi """)

st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")

st.sidebar.write("Developed using platforms:")
st.sidebar.image("https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png",width=120)

# Menu Home 
if menu == 'Home':
    st.image("https://lh3.googleusercontent.com/p/AF1QipMRzo0HFiToyXsOJdHRXDJ0FDPgZrZX0EMZkwmb=s1360-w1360-h1020", caption="Midnight in campus Ubakrie")
    st.markdown("---")

    st.header("Informasi Jadwal :")
    st.dataframe(jadwal_df)
    st.header("Daftar Tugas :")
    st.dataframe(tugas_df)

    st.markdown("---")
    st.header("Aplikasi untuk mengelola aktivitas kuliah")  
    st.write("Berguna untuk Membantu keseharian saya dalam mengelola jadwal serta tugas kuliah saya")

    st.image("https://www.ox.ac.uk/sites/files/oxford/styles/ow_large_feature/s3/field/field_image_main/Resources-for-staff-and-students.jpg?itok=kT5G8fHI")
    st.markdown("## Pada aplikasi web yang saya telah buat ada beberapa fitur yakni menu :")
    st.title("1. Hitung Nilai Akhir ")
    st.write("pada menu ini adalah saya membuat sebuah perhitungan nilai akhir UTS,UAS,dan Tugas. Dari ke tiga nilai tersebut akan di bagi 3 dengan bobot yang sudah ditentukan persis sama pada aplikasi big academik.")
    st.title("2. Kalkulator sederhana")
    st.write("pada menu ini adalah sebuah kalkulator sederhana yang biasa digunakan seperti pertambahan, pengurangan, perkalian dan pembagian. dengan menginput 2 nilai dan pilihan operasi.")
    st.title("3. Informasi Matkul")
    st.write("pada menu ini adalah untuk menambahkan,menampilkan serta menghapus mata kuliah, disini saya menjadi pengguna tujuan nya untuk dapat mengetahui serta mengedit jadwal matkul yang kita kelola sendiri. dan jika sewaktu-waktu ada makeup class bisa ditambahkan agar tetap selalu ingat")
    st.title("4. Tugas")
    st.write("pada menu ini adalah fungsi nya sama dengan informasi matkul hanya bedanya ini untuk menambahkan data tugas agar tidak lupa")

# Menu Hitung Nilai Akhir   
if menu == "Hitung Nilai Akhir":
    st.image("info.jpg")
    st.title('Penghitung Nilai Akhir')

    uts = st.number_input('Masukkan Nilai UTS:', min_value=0, max_value=100, value=0)
    uas = st.number_input('Masukkan Nilai UAS:', min_value=0, max_value=100, value=0)
    tugas = st.number_input('Masukkan Nilai Tugas:', min_value=0, max_value=100, value=0)

    if st.button('Total'):
        bobot_uts = 0.3
        bobot_uas = 0.4
        bobot_tugas = 0.3

        nilai_akhir = (uts * bobot_uts) + (uas * bobot_uas) + (tugas * bobot_tugas)
        st.write(f'Nilai Akhir Anda adalah: {nilai_akhir:.2f}')

#Menu Kalkulator
if menu == "Kalkulator":
    st.image("https://preview-assets-au-scc.kc-usercontent.com/330b87ea-148b-3ecf-9857-698f2086fe8d/b3a51c69-1aca-442d-a0f0-511d1c3e1c3a/maths_1920.jpg?w=1200&fm=webp")
    st.title('Kalkulator Sederhana')
    
    num1 = st.number_input('Masukkan Bilangan Pertama:', value=0)
    num2 = st.number_input('Masukkan Bilangan Kedua:', value=0)

    operasi = st.selectbox('Pilih Tindakan:', ('Penjumlahan', 'Pengurangan', 'Perkalian', 'Pembagian'))

    def calculate(num1, num2, operasi):
        if operasi == 'Penjumlahan':
            return num1 + num2
        elif operasi == 'Pengurangan':
            return num1 - num2
        elif operasi == 'Perkalian':
            return num1 * num2
        elif operasi == 'Pembagian':
            if num2 != 0:
                return num1 / num2
            else:
                st.error("Pembagian dengan nol tidak diperbolehkan.")
                return None

    if st.button('Hitung'):
        result = calculate(num1, num2, operasi)
        if result is not None:
            st.write(f'Hasil {operasi} antara {num1} dan {num2} adalah: {result:.1f}')

#menu informasi matkul 
if menu == "Kelola Matkul":
    st.image("https://img.pikbest.com/backgrounds/20220119/class-schedule-border-new-semester_6240001.jpg!sw800")
    st.subheader("Menu untuk mengelola aktivitas kuliah")

    st.title("Jadwal Harian Kampus")

    st.header("Tambah Jadwal Baru")
    
    with st.form(key='add_schedule_form'):
        schedule_id = st.number_input("ID Jadwal", min_value=1, step=1)
        date = st.text_input("Hari")
        time = st.time_input("Jam")
        subject = st.text_input("Mata Kuliah")
        location = st.text_input("Lokasi")
        submit_button = st.form_submit_button(label='Tambah Jadwal')

        if submit_button:
            jadwal_baru_ditambahkan = pd.DataFrame({
                "ID": [schedule_id],
                "Tanggal": [date],
                "Jam": [time],
                "Mata Kuliah": [subject],
                "Lokasi": [location]
            })
            jadwal_df = pd.concat([jadwal_df, jadwal_baru_ditambahkan], ignore_index=True)
            simpan_jadwal(jadwal_df)
            st.success("Jadwal berhasil ditambahkan!")
            st.dataframe(jadwal_df)
            
        

    st.header("Hapus Jadwal")
    with st.form(key='delete_schedule_form'):
        schedule_id_to_delete = st.number_input("ID Jadwal yang akan dihapus", min_value=1, step=1)
        delete_button = st.form_submit_button(label='Hapus Jadwal')

        if delete_button:
            jadwal_df = jadwal_df[jadwal_df["ID"] != schedule_id_to_delete]
            simpan_jadwal(jadwal_df)
            st.success("Jadwal berhasil dihapus!")
            st.dataframe(jadwal_df)

#menu informasi tugas 
if menu == "Kelola Tugas":
    st.image("https://png.pngtree.com/thumb_back/fh260/background/20210902/pngtree-countdown-to-the-college-entrance-examination-image_790187.jpg")

    st.header("Tambah Tugas Baru")
    with st.form(key='add_task_form'):
        task_id = st.number_input("ID Tugas", min_value=1, step=1)
        deadline = st.date_input("Deadline")
        nama_tugas = st.text_input("Nama tugas")
        ket_tugas = st.text_input("Keterangan")
        submit_task_button = st.form_submit_button(label='Tambah Tugas')

        if submit_task_button:
            tugas_baru_ditambahkan = pd.DataFrame({
                "ID": [task_id],
                "Deadline": [deadline],
                "Nama Tugas": [nama_tugas],
                "Keterangan": [ket_tugas]
            })
            tugas_df = pd.concat([tugas_df, tugas_baru_ditambahkan], ignore_index=True)
            simpan_tugas(tugas_df)
            st.success("Tugas berhasil ditambahkan!")
            st.dataframe(tugas_df)
    
    st.header("Hapus Tugas")
    with st.form(key='delete_task_form'):
        task_id_to_delete = st.number_input("ID Tugas yang akan dihapus", min_value=1, step=1)
        delete_task_button = st.form_submit_button(label='Hapus Tugas')

        if delete_task_button:
            tugas_df = tugas_df[tugas_df["ID"] != task_id_to_delete]
            simpan_tugas(tugas_df)
            st.success("Tugas berhasil dihapus!")
            st.dataframe(tugas_df)  

if menu == "Tools AI SIDAC":
    def ask(question):
        client = Groq(
            api_key='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'
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": question,
                },
            ],
            model="llama3-8b-8192",
        )

        return chat_completion.choices[0].message.content

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    st.title("Keperluan Tugas")
    st.markdown("### Alat parafrase teks")
    question = st.text_area("Masukkan teks:")

    button = st.button("Coba Parafrase")

    if button:
        answer = ask(f"tolong parafrasekan {question} jawab dengan bahasa indonesia")
        st.write(answer)

    st.title("Keperluan sehari-hari")
    st.markdown("### Alat menghitung ongkos dalam seminggu")
    question = st.text_input("Masukkan ongkos:")

    button = st.button("Coba hitung")

    if button:
        if question:
            if is_number(question):
                answer = ask(f"habis berapakah uang sebanyak {question} rupiah (IDR), dalam seminggu saya untuk ongkos,makan,dan tabungan? jawab dengan bahasa indonesia")
                st.write(answer)
            else:
                st.warning("Mohon masukkan angka yang valid untuk ongkos.")
        else:
            st.warning("Mohon diisi ongkos terlebih dahulu.")
            
if menu == "Tools Todo-list":
    db = Database()

    # Streamlit app logic
    st.title("Testing SQLite with Python App Todo-list")

    # Fetch tasks from the database
    data = db.view_task()

    # Input for new task
    task_input = st.text_input("Enter a new task:")
    btn = st.button("Add Task")

    # Add task if button clicked
    if btn:
        if task_input:
            db.add_task(task_input)
            st.experimental_rerun()
        else:
            st.error("Please enter a task.")

    # Display tasks with checkboxes
    for task in data:
        check = st.checkbox(f"{task[1]}", key=task[0])
        if check:
            db.delete_task(task[0])
            st.experimental_rerun()


    # def get_info():
    #     API_URL = 'https://newsapi.org/v2/top-headlines'
    #     API_KEY = '52a1da9884d645e38612e437214b8d89'

    #     params = {
    #         'apiKey' : API_KEY ,
    #         'country' : "id",
    #         'category' : "sports"
    #     }

    #     response = requests.get(API_URL, params=params)
    #     return response.json()['articles']

    # def ask(info):
    #     client = Groq(
    #         api_key='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'
    #     )

    #     chat_completion = client.chat.completions.create(
    #         messages=[
    #             {
    #                 "role": "system",
    #                 "content": "you are news summarizer",
    #             },
    #             {
    #                 "role": "user",
    #                 "content": f"### Here is the news: \n {info}    \n ### SUMMARIZE THE NEWS",
    #             },
    #         ],
    #         model="llama3-8b-8192",
    #     )

    #     return chat_completion.choices[0].message.content

    # button = st.button("Get news latest news information")

    # if button:
    #     answer = ask(get_info())
    #     st.write(answer)