import pandas as pd
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# JSON文件的路径
file_path2 = '..realtimeData/output_formatted.json'

# 读取JSON文件
with open(file_path2, 'r') as file:
    data = json.load(file)

# 提取_source中的内容
records = [item["_source"] for item in data]

# 将记录转换为DataFrame
df2 = pd.DataFrame(records)

regions = [
    "aireys inlet",
    "avalon",
    "ballarat",
    "cerberus",
    "coldstream",
    "essendon airport",
    "fawkner beacon",
    "ferny creek",
    "frankston",
    "frankston beach",
    "geelong racecourse",
    "laverton",
    "melbourne airport",
    "melbourne",
    "moorabbin airport",
    "point cook",
    "point wilson",
    "pound creek",
    "rhyll",
    "scoresby",
    "sheoaks",
    "south channel island",
    "st kilda harbour rmys",
    "viewbank",
    "wonthaggi"
]

# 查找包含任意一个地区标签的行
contains_regions = df2['tags'].apply(lambda tags: any(region in tags for region in regions))

# 获取这些行的索引
rows_with_regions = df2[contains_regions]

# 查看结果
df= rows_with_regions



from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# 将 tokens 列转换为字符串
df['text'] = df['tokens'].apply(lambda x: ' '.join(x))

# 使用 CountVectorizer 创建词袋模型，并去掉停用词
vectorizer = CountVectorizer(stop_words='english')  # 或者使用自定义停用词列表：stop_words=my_stop_words_list
X = vectorizer.fit_transform(df['text'])

# 使用 LDA 进行主题建模
lda = LatentDirichletAllocation(n_components=2, random_state=42)
lda.fit(X)

# 打印主题中的词语
for idx, topic in enumerate(lda.components_):
    print(f"Topic #{idx + 1}:")
    print([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-11:-1]])




## 画图

plt.figure(figsize=(10, 6))
df['sentiment'].hist(bins=30, edgecolor='black')

# 设置图表标题和标签
plt.title('Sentiment Score Distribution')
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')

# 显示图表
plt.show()

print(df.describe())

# 将 tokens 列中的词语拼接成一个字符串
text = ' '.join([' '.join(tokens) for tokens in df['tokens']])

# 生成词云
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# 绘制词云
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()



# 定义与空气质量和天气相关的关键词
keywords = [
    'pm2.5', 'pm10', 'air', 'pollution', 'quality', 'smog', 'haze', 'weather',
    'temperature', 'humidity', 'rain', 'snow', 'wind', 'storm', 'forecast', 'sunny',
    'cloudy', 'visibility', 'particulate', 'ozone', 'dust', 'allergen', 'thunderstorm',
    'precipitation', 'climate', 'fog', 'barometer', 'dew', 'UV', 'index', 'aerosol',
    'heatwave', 'cold front', 'high pressure', 'low pressure'
]

# 提取相关信息
def extract_relevant_tokens(tokens, keywords):
    return [token for token in tokens if token.lower() in keywords]

df['relevant_tokens'] = df['tokens'].apply(lambda x: extract_relevant_tokens(x, keywords))

# 过滤包含相关关键词的行
relevant_rows = df[df['relevant_tokens'].apply(lambda x: len(x) > 0)]

# 将包含相关关键词的行变成新的 DataFrame
relevant_df = relevant_rows.reset_index(drop=True)

# 将 tokens 列中的词语拼接成一个字符串
text = ' '.join([' '.join(tokens) for tokens in relevant_df['tokens']])

# 生成词云
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# 绘制词云
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

plt.figure(figsize=(10, 6))
relevant_df['sentiment'].hist(bins=30, edgecolor='black')

# 设置图表标题和标签
plt.title('Sentiment Score Distribution')
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')

# 显示图表
plt.show()