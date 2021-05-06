from newapp.models import *

# Создать двух пользователей (с помощью метода User.objects.create_user).
user01 = User.objects.create(username = 'User01Name', first_name = 'Ivan')
# user01 = User.objects.get(username = 'User01Name', first_name = 'Ivan') # Если уже есть объект, его можно присвоить GET
user02 = User.objects.create(username = 'User02Name', first_name = 'Peter')

# Создать два объекта модели Author, связанные с пользователями.
author01 = Author.objects.create(authorUser = user01)
author02 = Author.objects.create(authorUser = user02)

# Добавить 4 категории в модель Category.
categorySport = Category.objects.create(categoryName = 'Sport')
categoryPolitic = Category.objects.create(categoryName = 'Politic')
categorySociety = Category.objects.create(categoryName = 'Society')
categoryScience = Category.objects.create(categoryName = 'Science')

# Добавить 2 статьи и 1 новость.
post01Article = Post.objects.create(postAuthor = author01, postType = 'AR', postTitle = 'ArticleTitle01', postText = 'ArticleText01')
post02Article = Post.objects.create(postAuthor = author02, postType = 'AR', postTitle = 'ArticleTitle02', postText = 'ArticleText02')
post03News = Post.objects.create(postAuthor = author01, postType = 'NE', postTitle = 'NewsTitle03', postText = 'NewsText03')

# Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
post01Article.postCategory.add(categorySport, categoryPolitic)
post02Article.postCategory.add(categorySociety, categoryScience)
post03News.postCategory.add(categoryPolitic, categorySociety)

# Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
comment01 = Comment.objects.create(commentUser = user01, commentPost = post01Article, commentText = 'commentText01')
comment02 = Comment.objects.create(commentUser = user02, commentPost = post01Article, commentText = 'commentText02')
comment03 = Comment.objects.create(commentUser = user01, commentPost = post02Article, commentText = 'commentText03')
comment04 = Comment.objects.create(commentUser = user02, commentPost = post03News, commentText = 'commentText04')

# Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
post01Article.like()
post01Article.like()
post01Article.like()
post01Article.dislike()
post02Article.dislike()
post02Article.dislike()
post02Article.dislike()
post02Article.dislike()
post02Article.like()
post03News.like()
post03News.like()
post03News.dislike()

comment01.like()
comment01.dislike()
comment01.like()
comment02.like()
comment02.like()
comment02.like()
comment02.like()
comment03.dislike()
comment03.dislike()
comment03.dislike()
comment04.like()
comment04.like()
comment04.like()
comment04.like()
comment04.dislike()

# Обновить рейтинги пользователей.
author01.update_rating()
author02.update_rating()

# Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
Author.objects.all().order_by('-authorRating').values('authorUser__username', 'authorRating')[0]

# Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
sortingPosts = Post.objects.all().order_by('-postRating')
bestPost = sortingPosts.values('postDTCreate', 'postAuthor__authorUser__username', 'postRating', 'postTitle', 'postText')[0]
bestPost.update({'postPreview': sortingPosts[0].preview()})
bestPost

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
Comment.objects.filter(commentPost=sortingPosts[0]).values('commentDTCreate', 'commentUser__username', 'commentRating', 'commentText')



# Чистка ранее записанных объектов (чтобы начать без данных)
# User.objects.all().delete()
# Category.objects.all().delete()