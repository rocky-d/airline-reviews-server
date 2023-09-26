from typing import Iterable

import pandas as pd
from redis import Redis, ConnectionPool, StrictRedis
from wordcloud import WordCloud


def get_rp() -> ConnectionPool | None:
    redis_pool: ConnectionPool | None = None
    try:
        redis_pool = ConnectionPool(
            host = '192.168.0.115',
            port = 6379,
            db = 1)
        print('Redis database connected!')
    except Exception as e:
        print(e)
    finally:
        return redis_pool


def iter_redis_list(redis_client: Redis, list_key: str) -> Iterable[str]:
    for index in range(redis_client.llen(list_key)):
        yield redis_client.lindex(list_key, index)


def update_redis_list(redis_client: Redis, list_key: str, new_list: list[str]) -> None:
    redis_client.delete(list_key)
    for row in new_list:
        redis_client.rpush(list_key, row)


def get_reviews_for_airline(redis_client: Redis, arl_name: str) -> str:
    res = ''

    arl_name = arl_name.lower()
    df = pd.read_csv(r'data_csv/AIRLINEREVIEWS_DB/AIRLINE.csv')
    # for arl_json in iter_redis_list(redis_client, 'AIRLINE'):
    #     arl_dict = json.loads(arl_json)
    for index, row in df.iterrows():
        arl_dict = row.to_dict()
        if arl_name == arl_dict['ARL_NAME'].lower():
            airl_iata = arl_dict['ARL_IATA']
            break
    else:
        return 'AIRLINE_NOT_FOUND'

    df = pd.read_csv(r'data_csv/AIRLINEREVIEWS_DB/REVIEW.csv')
    # for rev_json in iter_redis_list(redis_client, 'REVIEW'):
    #     rev_dict = json.loads(rev_json)
    for index, row in df.iterrows():
        rev_dict = row.to_dict()
        if airl_iata == rev_dict['REV_FLT_ARL_IATA']:
            res += rev_dict['REV_TITLE'] + ' ' + rev_dict['REV_CONTENT'] + ' '

    return (res
            .replace('\'', ' ')
            .replace('.', ' ')
            .replace(',', ' ')
            .replace(':', ' ')
            .replace(';', ' ')
            .strip())


def generate_word_cloud(text: str, path: str, arl_name: str, width: str = 1920, height: str = 1080,
                        bc: str = 'white') -> str:
    # 假设你有一个大的字符串变量 text
    # 这里简单地使用空格来拆分文本为单词，你可以根据需要进行更复杂的文本处理
    words = text.lower().split()  # 将文本拆分成单词列表

    word_freq = {}  # 用于存储单词频率的字典

    for word in words:
        # 使用字典来计算单词的频率
        if word in ['good', 'bad', 'awesome', 'happy', 'nice', 'worst', 'mad', 'angry', 'best']:
            word_freq[word] = word_freq.get(word, 0) + 5
        else:
            word_freq[word] = word_freq.get(word, 0) + 1

    # 常见的无关紧要的单词列表
    common_words_to_exclude = [
        'the', 'and', 'on', 'in', 'we', 'you', 'he', 'she', 'it', 'they', 'their',
        'is', 'are', 'was', 'were', 'to', 'of', 'for',
        'with', 'as', 'at', 'by',
        'this', 'that', 'an', 'a', 'or', 'but', 'from', 'not', 'so', 'just',
        'will', 'can', 'should', 'could', 'would', 'am', 'be', 'have', 'has',
        'had', 'do', 'does', 'did', 'here', 'there', 'now', 'then', 'than',
        'our', 'very', 'my', 'me', 'too', 'if', 'didn', 'did', 'a', 'b', 'c',
        'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
        'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'his', 'her', 'mine', 'its',
        'about', 'some', 'thing', 'because', 'been', 'being', 'don', 'ife', 'them'
    ]  # 添加更多你认为不需要包含在词云中的单词

    # 移除无关紧要的单词
    filtered_word_freq = {word: freq for word, freq in word_freq.items()
                          if word not in common_words_to_exclude}

    try:
        width = int(width)
    except Exception as e:
        print(e)
        width = 1920
    try:
        height = int(height)
    except Exception as e:
        print(e)
        height = 1080
    try:
        bc = bc.upper()
        if bc not in ['WHITE', 'BLACK', 'YELLOW', 'RED', 'GREEN', 'BLUE', 'PINK']:
            raise Exception
    except Exception as e:
        print(e)
        bc = 'WHITE'

    # 创建一个WordCloud对象并生成词云图像
    wordcloud = WordCloud(width = width, height = height, background_color = bc)
    wordcloud.generate_from_frequencies(filtered_word_freq)

    # 保存词云图像到当前目录
    wordcloud.to_file(path)
    print('wordcloud.png saved')
    return f'{bc.lower().title()} Word Cloud of the Reviews for {arl_name.lower().title()}'
