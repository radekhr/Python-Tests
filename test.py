# int
lesson_nr = 1
print(lesson_nr, type(lesson_nr))

# string

lesson_name = "python tutorial"
print(lesson_name, type(lesson_name))

# list

tweet_lenghts = [45, 54, 123, 1033]
print(tweet_lenghts, type(tweet_lenghts))
print(tweet_lenghts[1])

# tuple (krotki)

tweet_lenghts_immutable = (45, 54, 123, 1033)
print(tweet_lenghts_immutable, type(tweet_lenghts_immutable))

# dict

tweets_by_user = {
    # klucz : wartosc
    'Jan' : [1, 14],
    'Maria' : [56, 3]
}

print(tweets_by_user, type(tweets_by_user))
print(tweets_by_user['Jan'])

for tweet in tweet_lenghts:
    print(tweet)

def custom_print(var, list_var = None, *args, **kwargs):
    print("Start")
    print(var)
    if list_var:
        for el in list_var:
            print("LIST VAR", el)
    print("ARGS", args)
    print("KWARGS", kwargs)
    print("End")

custom_print(1)
custom_print(1, [1, 2, 3])
custom_print(1, [1, 2, 3], 'arg3', 4, arg5=6, arg6={'test':'bla'} )






