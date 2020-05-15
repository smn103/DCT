import random
import string

def random_string_generator():
    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    result=''
    for i in range(0, 11):
        result += random.choice(characters)
    
    return result



def unique_video_id_generator(instance):
    video_new_id= random_string_generator()

    Klass= instance.__class__

    qs_exists= Klass.objects.filter(videoid= video_new_id).exists()
    if qs_exists:
        return unique_video_id_generator(instance)
    return video_new_id