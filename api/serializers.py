from rest_framework import serializers

from .models import Categories, Comment, Genres, Review, Titles, User


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genres


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genres.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all())

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category',)


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True)
    category = CategoriesSerializer()
    rating = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Titles
        fields = (
            'id', 'name', 'year',
            'description', 'genre', 'category', 'rating',
        )


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='description'
    )
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    def create(self, data):
        name = self.context["view"].kwargs.get("title_id")
        author = self.context["request"].user
        message = 'Author review already exist'
        if Review.objects.filter(title=name, author=author).exists():
            raise serializers.ValidationError(message)
        return Review.objects.create(**data)

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(many=False,
                                          read_only=True,
                                          slug_field='username')

    review = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='text'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class UserCodeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'pk', 'first_name',
                  'last_name', 'email', 'role', 'bio')
        model = User


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)
