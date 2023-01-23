import requests
import string

def get_points_for_time(video_data, period):
    """

    :return:
    """
    list_time_periods = [item for item in video_data["Time_period"]]
    return list_time_periods.count(period)


def get_points_for_creator(video_data, creator):
    """

    :return:
    """

    videos_watched_by_creator = 0
    videos_made_by_creator = 0

    for i, item in enumerate(video_data.values):
        if str.lower(item[1]) == str.lower(creator):
            videos_made_by_creator += 1
            if item[-1] == "yes":
                videos_watched_by_creator += 1

    return videos_watched_by_creator / videos_made_by_creator


def read_common_words():
    with open("Actors.txt", "r") as fr:
        content_1 = fr.readlines()
    return [item.strip() for item in content_1]


def get_points_for_name(words_list, name):
    """

    :return:
    """
    name_list_with_symbols = name.split(" ")
    name_list = []
    points = 0
    for item in name_list_with_symbols:
        for ch in item:
            if ch in string.punctuation:
                item = item.strip(ch)
        name_list.append(item)

    for item in name_list:
        if item.lower() in words_list and item.lower() not in ["and", "for", "of", "is", "are", "the", "to", "was",
                                                               "at", "this", "a", "an", "with", "will", "would", "were",
                                                               "as", "in", "not", "yes", "no", "or", "like", "for",
                                                               "then"

                                                               "i", "you", "he", "she", "it", "we", "they", "us",
                                                               "them", "your", "yours", "me"

                                                                                        "why", "what", "which", "who",
                                                               "where", "when", "how",
                                                               "whose", "whom"]:
            points += 1

    print(points)
    return points
