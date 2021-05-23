from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Twitter API setup
consumerKey = "uxCOp2lfm4Dvw71yVuWU0pgzZ"
consumerSecret = "9qveoMlUbGEUQEiaaMVAdBlt1LK7V5BK5cCWLWKIFucZ28sCzD"
accessToken = "903670332996726785-tB32oiJ2MQN2bIqp9lLg1oq02sX7SgV"
accessTokenSecret = "LADdVnkIj5TCPqGS1bYbDf80dQhgYQx9nfQS31u2DWUit"
authenticate = tweepy.OAuthHandler(consumer_key=consumerKey, consumer_secret=consumerSecret)
authenticate.set_access_token(key=accessToken, secret=accessTokenSecret)
api = tweepy.API(authenticate, wait_on_rate_limit=True)

#GUI Setup
root = Tk()
root.title('Tweet Analysis :A Sentiment Analysis Tool')

root.geometry("1366x768")
root.resizable(True, True)

main_frame = Frame(root, width=1920, height=1000)
main_frame.place(x=0, y=0)

my_canvas = Canvas(main_frame, width=1920, height=1000)
my_canvas.place(x=0, y=0)

my_scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.place(relx=0.9890, y=0, relheight=0.9895)

my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

# def _on_mouse_wheel(event):
#     my_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")


# my_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)
second_frame = Frame(my_canvas, width=1920, height=1000)
second_frame.place(x=0, y=0)
my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
second_frame.configure(height=2000)
logoimg = PhotoImage(file='Sentiment Analysis\\resources\\logo.png')
topLabel = PhotoImage(file="Sentiment Analysis\\resources\\topLabel.png")
titleLabel = Label(second_frame, text="Tweet Sentiment Analysis", image=topLabel, compound='left',font=('', 35, 'bold'), fg='#2ba6df').place(x=0, y=0)
root.iconphoto(False, logoimg)
HandlePrompt = Label(second_frame, text="Twitter handle @",font=('', 18, '')).place(x=10, y=150)
twitterHandle = Entry(second_frame, font=('', 16, ''), border=5, width=18)
twitterHandle.place(x=200, y=150)

def analyse_tweets():
    fetch = api.user_timeline(
        screen_name=twitterHandle.get(), count=100, tweet_mode="extended")
    posts = []
    for lines in fetch:
        if lines.lang == "en":
            posts.append(lines)
    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

    def clean_txt(text):
        text = re.sub('@[A-Za-z0–9]+', '', text)
        text = re.sub('#', '', text)
        text = re.sub('RT[\s]+', '', text)
        text = re.sub('https?:\/\/\S+', '', text)
        return text

    df['Tweets'] = df['Tweets'].apply(clean_txt)

    def get_subjectivity(text):
        return round(TextBlob(text).sentiment.subjectivity, 3)

    def get_polarity(text):
        return round(TextBlob(text).sentiment.polarity, 3)

    df['Subjectivity'] = df['Tweets'].apply(get_subjectivity)
    df['Polarity'] = df['Tweets'].apply(get_polarity)

    def get_analysis(score):
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'

    df['Analysis'] = df['Polarity'].apply(get_analysis)
    return df


def show_table():
    table = analyse_tweets()
    cols = list(table.columns)
    table.to_csv(f"{twitterHandle.get()}.csv")
    table.squeeze()
    table.index += 1
    table = table.iloc[::-1]
    tree = ttk.Treeview(second_frame, show=["headings"])
    tree.place(relwidth=0.548, x=348, y=220)
    tree["columns"] = cols

    tree.heading(0, text="Tweets", anchor='w')
    tree.heading(1, text="Subjectivity", anchor='center')
    tree.heading(2, text="Polarity", anchor='center')
    tree.heading(3, text="Analysis", anchor='center')
    tree.column(0, anchor="w", width=600, stretch=NO)
    tree.column(1, anchor="center", width=150, stretch=NO)
    tree.column(2, anchor="center", width=150, stretch=NO)
    tree.column(3, anchor="center", width=150, stretch=NO)

    for index, row in table.iterrows():
        tree.insert("", 0, text=index, values=list(row))


analyse = Button(second_frame, text='Analyse', font=('', 12, 'bold'), relief='raised', command=show_table,activebackground='#2ba6df', bd=4)
analyse.place(x=440, y=150)


def word_cloud():
    global dire
    df = analyse_tweets()
    allWords = ' '.join([twts for twts in df['Tweets']])
    wordCloud = WordCloud(width=1000, height=360,random_state=21, max_font_size=110).generate(allWords)
    plt.imshow(wordCloud, interpolation="bilinear")
    plt.axis('off')
    wordCloud.to_file(
        f'C:\\Users\\SAUR\\Documents\\SEM 4\\Sentiment Analysis\\src\\wordCloudGenerates\\{twitterHandle.get()}.png')
    image1 = Image.open(
        f'C:\\Users\\SAUR\\Documents\\SEM 4\\Sentiment Analysis\\src\\wordCloudGenerates\\{twitterHandle.get()}.png')
    test = ImageTk.PhotoImage(image1)
    label1 = Label(second_frame, image=test)
    label1.image = test
    label1.place(x=360, y=1450)


show_cloud = Button(second_frame, text='Word Cloud', font=('', 16, 'bold'), relief='raised', command=word_cloud,activebackground='#2ba6df', bd=4)
show_cloud.place(x=780, y=1380)


def scattered_graph():
    df = analyse_tweets()
    fig1 = plt.figure(figsize=(6, 8), dpi=100)
    ax1 = fig1.add_subplot(111)
    ax1.scatter(df['Polarity'], df['Subjectivity'], color='g')
    scatter1 = FigureCanvasTkAgg(fig1, second_frame)
    scatter1.get_tk_widget().place(x=210, y=550)
    ax1.legend(['Analysis'])
    ax1.set_xlabel('Polarity')
    ax1.set_ylabel('Subjectivity')
    ax1.set_title('Polarity vs Subjectivity')


show_scatter = Button(second_frame, text='Scattered Graph Analysis', font=('', 16, 'bold'), relief='raised',command=scattered_graph, activebackground='#2ba6df', bd=4)
show_scatter.place(x=400, y=500)


def show_bar():
    df = analyse_tweets()
    barFig = plt.figure(figsize=(6, 8), dpi=100)
    ax1 = barFig.add_subplot(111)
    bar1 = FigureCanvasTkAgg(barFig, second_frame)
    bar1.get_tk_widget().place(x=900, y=550)
    df = df[['Analysis']].value_counts()
    df.plot(kind='bar', legend=False, ax=ax1)
    ax1.set_title('Polarity Analysis')
    ax1.set_xlabel('Polarity')
    ax1.set_ylabel('Counts')


show_barGraph = Button(second_frame, text='Bar Graph Analysis', font=('', 16, 'bold'), relief='raised',command=show_bar, activebackground='#2ba6df', bd=4)
show_barGraph.place(x=1100, y=500)

root.mainloop()