from bleach.sanitizer import Cleaner
from django.utils.translation import ugettext_lazy as _
from django.db.models import Max
from django.conf import settings
from api.paginators import *
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from api.models import *


class BasicProfileSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        required=False
    )

    class Meta:
        model = Profile
        fields = ('id', 'display_name', 'picture', 'account')


class GroupForumBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupForum
        fields = ('id', 'name', 'image')


class AccountSerializer(CountryFieldMixin, serializers.ModelSerializer):
    profile = BasicProfileSerializer()

    member_groups = GroupForumBasicSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Account
        fields = ('id', 'username', 'country', 'email', 'profile', 'friends', 'member_groups'
)
    def to_representation(self, obj):
        if self.context.get('is_anonymous', False):
            return {
                'id': -1,
                'username': 'Anonymous',
                'country': '',
                'email': ''
            }

        return super(AccountSerializer, self).to_representation(obj)


class FullAccountSerializer(AccountSerializer):
    """Requires full account view permissions (i.e. admin or current user privilege levels) UNLESS it is from a CREATE request."""
    account_settings = serializers.JSONField(read_only=False)

    def create(self, validated_data):
        profile_data = {}
        if 'profile' in validated_data:
            profile_data = validated_data.pop('profile')

        password = validated_data.pop('password')
        account = Account.objects.create(**validated_data)
        account.set_password(password)

        profile = Profile.objects.create(**profile_data, account=account)
        account.profile = profile
        account.save()

        return account

    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'password', 'country', 'account_settings', 'profile')


class PrivateAccountProfileDetailsSerializer(serializers.ModelSerializer):
    account_settings = serializers.JSONField(read_only=False)
    profile = BasicProfileSerializer()

    class Meta:
        model = Account
        fields = ('id', 'account_settings', 'profile', 'member_groups')


class LogSerializer(serializers.Serializer):
    created = serializers.DateTimeField()
    last_modified = serializers.DateTimeField()
    message = serializers.CharField(max_length=400, allow_blank=True)


class ActivityLogSerializer(serializers.ModelSerializer):
    action = serializers.CharField(source='get_action_display')

    class Meta:
        model = ActivityLog
        fields = ('id', 'action', 'message', 'context', 'author')


class BlogPostSerializer(serializers.Serializer):
    title = serializers.CharField()
    slug = models.SlugField()
    # TODO create authors field validator
    authors = serializers.ListField(
        child=serializers.CharField()
    )
    body = serializers.CharField()


# class MediaSrcHyperlinkedField(serializers.HyperlinkedIdentityField):
#     def to_representation(self, data):
#         pass

#     def to_internal_value(self, data):
#         return

#     def get_url(self, obj, view_name, request, format):
#         return 'https:/i.imgur.com/5EMmiqE.png'
#         # TODO do I need the album primary key here?
#         # url_kwargs = {
#         #     'album_pk': obj.pk,
#         #     'media_pk': obj.pk
#         # }
#         # return reverse()

#     def get_object():
#         pass


class MediaListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        # Batch upload is being performed
        media_list = [Media(**item) for item in validated_data]
        try:
            return Media.objects.create
        except (TypeError) as e:
            return Media.objects.bulk_create(media_list)

    def update(self, instance, validated_data):
        # is this where we check if the filetype is valid etc.?

        # multiple media updates are happening at once
        pass


class MediaAllowedFileTypeChecker(object):
    ALLOWED_FILETYPES = settings.ACCEPT_FILETYPES

    def __contains__(self, val):
        for kind, types in settings.ACCEPT_MIMES.values():
            if val in types:
                return kind
        raise ValidationError("Media type could not be determined.")


# class MediaSrcField(FileField):
#     ALLOWED_TYPES = MediaAllowedFileTypeChecker()

#     def get_file_extension(self, filename, decoded_file):
#         #
#         # WARNING: this could be DDOSed!
#         #
#         from django.core.files.storage import default_storage
#         from django.core.files.base import ContentFile
#         from os.path import join
#         import magic
#         tmpfile = 'tmp/{}'.format(upload)
#         default_storage.save(tmpfile, ContentFile(decoded_file).read())
#         path_to_tmpfile = join(settings.MEDIA_ROOT, tmpfile)

#         file_mime = magic.from_file(path_to_tmpfile, mime=True)

#         return file_mime

#     def to_internal_value(self, data):
#         file_object = super(MediaSrcField, self).to_internal_value(data)
#         # TODO add virus protection

#         try:
#             file_object['ext'] = file_object['name'].split('.')[1 ]
#         except IndexError:
#             # There is no explicit file extension
#             file_object['ext'] = ''

#         if 'mime' not in file_object:
#             # Try to figure out a file format from the associated mimetypes
#             file_object['mime'] = self.infer_format(data.file)

#         return file_object


# class MediaHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
#     src = MediaSrcHyperlinkedField(
#         read_only=False,
#         many=True,
#         required=False,
#         view_name='media-image-src'
#     )

#     tags = serializers.PrimaryKeyRelatedField(
#         queryset=MediaTag.objects.all(),
#         many=True,
#         required=False
#     )

#     class Meta:
#         model = Media
#         list_serializer_class = MediaListSerializer
#         fields = ('album', 'title', 'description', 'tags', 'media_type', 'src')


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('id', 'title', 'description', 'tags', 'media_type')

    def determine_media_type(self, mime):
        for kind, types in settings.ACCEPT_MIMES.values():
            if mime in types:
                return kind
        raise ValidationError("Media type could not be determined.")

    # def validate(self, data):
    #     if data['media_type'] not in mediaChoices:
    #         data['media_type'] = self.determine_media_type(data['src']['mime'])

        # if data['src']['size'] > settings.MAX_FILE_SIZE[data['media_type']]:
        #     raise ValidationError('File cannot be stored due to large size')

        # acceptable_mimes = settings.ACCEPT_MIMES[data["media_type"]]
        # if data['src']['mime'] not in acceptable_mimes:
        #     raise ValidationError('MIME type not valid for media_type')


class AlbumMediaBrowserPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 24
    # essentially we limit this because this will be 24 "guaranteed" CDN requests


# class MediaBrowserSerializer(serializers.HyperlinkedModelSerializer):
#     media_set = SerializerMethodField()


#    class Meta:
#         model = Album
#         # TODO reevaluate this later
#         #'thumbnail', 
#         fields = ('media_set')

    # def get_media_set(self, obj):
    #     MediaSerializer(
    #         many=True,
    #         read_only=True
    #     )

    #     return serializer.data

class AlbumInfoSerializer(serializers.ModelSerializer):
    owner = AccountSerializer(
        read_only=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=AlbumTag.objects.all(),
        many=True,
        required=False
    )
    class Meta:
        model = Album
        fields = ('id', 'title', 'description', 'owner', 'tags')


class AlbumCreateSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        required=False
    )

    tags = serializers.PrimaryKeyRelatedField(
        queryset=AlbumTag.objects.all(),
        many=True,
        required=False
    )
    class Meta:
        model = Album
        fields = ('id', 'title', 'description', 'owner', 'tags')


class FeedContentItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedContentItemType
        fields = ('id', 'name')


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ('id', 'name')


class PlaceSerializer(serializers.ModelSerializer):
    owner = AccountSerializer()

    class Meta:
        model = Place
        fields = ('id', 'name', 'owner', 'default_feed')


class ProfileSerializer(serializers.ModelSerializer):
    interests = InterestSerializer(
        many=True
    )

    class Meta:
        model = Profile
        fields = ('id', 'display_name', 'account', 'picture', 'title', 'description', 'interests')


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'display_name', 'account', 'picture', 'title', 'description', 'interests')


class FeedCreateUpdateSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        required=False
    )

    content_types = serializers.PrimaryKeyRelatedField(
        queryset=FeedContentItemType.objects.all(),
        many=True,
        required=False
    )

    stashes = serializers.PrimaryKeyRelatedField(
        queryset=FeedContentStash.objects.all(),
        many=True,
        required=False
    )

    places = serializers.PrimaryKeyRelatedField(
        queryset=Place.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Feed
        fields = ('id', 'name', 'description', 'owner', 'content_types', 'interests', 'places', 'stashes', 'visibility')

    def to_representation(self, obj):
        result = super(FeedCreateUpdateSerializer, self).to_representation(obj)

        # Filter to only include places that are owned by this user
        request = self.context.get("request")
        if request and hasattr(request, 'user'):
            result['places'] = [place.id for place in obj.places.filter(owner=request.user)]

        return result


class FeedSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        required=False
    )

    interests = InterestSerializer(
        many=True
    )

    class Meta:
        model = Feed
        fields = ('id', 'name', 'description', 'owner', 'content_types', 'created', 'interests', 'stashes', 'visibility')


class CommentBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'owner', 'is_anonymous', 'content_item', 'user_profile', 'parent', 'text', 'created')

    def to_representation(self, obj):
        # TODO make this a mixin?
        self.context['is_anonymous'] = obj.is_anonymous

        result = super(CommentBasicSerializer, self).to_representation(obj)

        # If this is the primary key serializer, give it the forgotten fake intance
        if obj.is_anonymous and isinstance(result['owner'], int):
            result['owner'] = {
                'id': -1,
                'username': 'Anonymous',
                'country': '',
                'email': ''
            }

        return result


class CommentSerializer(CommentBasicSerializer):
    owner = AccountSerializer(
        read_only=True
    )


class CommentCreateUpdateSerializer(CommentBasicSerializer):
    pass


class FeedContentItemBasicSerializer(serializers.ModelSerializer):

    content_type = serializers.PrimaryKeyRelatedField(
        queryset=FeedContentItemType.objects.all(),
        required=False
    )
    is_anonymous = serializers.BooleanField(
        required=False
    )
    class Meta:
        model = FeedContentItem
        fields = ('id', 'title', 'description', 'owner', 'is_anonymous', 'content_type', 'visibility', 'created', 'interests', 'places')

    def to_representation(self, obj):
        self.context['is_anonymous'] = obj.is_anonymous
        result = super(FeedContentItemBasicSerializer, self).to_representation(obj)

        # Filter to only include places that are owned by this user
        request = self.context.get("request")
        if request and hasattr(request, 'user'):
            result['places'] = [place.id for place in obj.places.filter(owner=request.user)]

        # If this is the primary key serializer, give it the forgotten fake intance
        if obj.is_anonymous and isinstance(result['owner'], int):
            result['owner'] = {
                'id': -1,
                'username': 'Anonymous',
                'country': '',
                'email': ''
            }

        return result

def get_content_id(instance):
    _model = None
    if instance.content_type.name == FeedContentItemType.TOPIC or \
       instance.content_type.name == FeedContentItemType.POST:
        _model = Discussion
    elif instance.content_type.name == FeedContentItemType.LINK:
        _model = Link
        # elif instance.content_type == FeedContentItemType.IMAGE:
        #     _model =

    pk = _model.objects.filter(content_item=instance).values_list('id', flat=True).first()
    return pk

def get_group_id(instance):
    valid_stashes = FeedContentStash.objects.filter(owned_content__in=(instance,), feeds__isnull=False)
    if valid_stashes.count() > 0:
        valid_feeds = Feed.objects.filter(stashes__in=valid_stashes, groupforum__isnull=False)

        if valid_feeds.count() > 0:
            feed = valid_feeds.first()
            return feed.groupforum_set.first().id

def get_feed_id(instance):
    if instance.origin_stash:
        return instance.origin_stash.feeds.first().id


class FeedContentItemSerializer(FeedContentItemBasicSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        required=False
    )
    object_id = serializers.SerializerMethodField('get_content_id')
    origin_stash_id = serializers.SerializerMethodField()
    feed_id = serializers.SerializerMethodField()
    group_id = serializers.SerializerMethodField()
    is_local = serializers.SerializerMethodField()
    nested_object = serializers.SerializerMethodField()
    # content_type = serializers.StringRelatedField(
    #     required=False
    # )

    class Meta:
        model = FeedContentItem
        fields = ('id', 'title', 'description', 'owner', 'is_anonymous', 'is_local', 'content_type', 'comments', 'created', 'object_id', 'origin_stash_id', 'feed_id', 'group_id', 'nested_object', 'visibility', 'interests')

    def get_content_id(self, instance):
        return get_content_id(instance)

    def get_origin_stash_id(self, instance):
        if instance.origin_stash:
            return instance.origin_stash.id

    def get_feed_id(self, instance):
        return get_feed_id(instance)

    def get_group_id(self, instance):
        return get_group_id(instance)

    def get_is_local(self, instance):
        allowed_places = self.context.get('allowed_places', [])

        for place_id in [p.id for p in instance.places.all()]:
            if place_id in allowed_places:
                return True

        return False

    def get_nested_object(self, instance):
        """Returns a nested representation of the content item's object"""
        if instance.content_type.name == FeedContentItemType.LINK:
            content_id = self.get_content_id(instance)
            if content_id:
                return BasicLinkSerializer(instance=Link.objects.get(id=self.get_content_id(instance))).data


class FeedContentItemCreateUpdateSerializer(FeedContentItemSerializer):
    comments = CommentSerializer(
        many=True,
        read_only=True,
        required=False
    )


class FeedContentItemProfileSerializer(FeedContentItemBasicSerializer):
    owner = AccountSerializer()
    comments = CommentSerializer(
        many=True,
        read_only=True,
        required=False
    )

    class Meta:
        model = FeedContentItem
        fields = ('id', 'title', 'description', 'owner', 'interests', 'comments', 'content_type', 'created', 'is_anonymous', 'visibility')


class FeedContentStashSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField('paginated_content')

    class Meta:
        model = FeedContentStash
        fields = ('id', 'name', 'description', 'content')

    def paginated_content(self, instance):
        request = self.context['request']

        content_queryset = instance.content.all()
        _content_types = request.data.get('content_types', None)
        if _content_types:
            content_queryset = content_queryset.filter(content_type__in=FeedContentType.objects.filter(id__in=_content_types))

        _interests = request.data.get('interests', None)
        if _interests:
            content_queryset = content_queryset.filter(interests__in=Interest.objects.filter(id__in=_interests))

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(content_queryset, self.context['request'])
        serializer = FeedContentItemSerializer(
            page,
            many=True,
            context={'request': self.context['request']}
        )
        return serializer.data


class FeedContentStashCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedContentStash
        # NOTE one request could wipe out entire stash! BAD
        fields = ('id', 'name', 'description', 'content')


class ContentItemCRUDSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        if 'content_item' in validated_data:
            for k,v in validated_data.pop('content_item').items():
                setattr(instance.content_item, k, v)
                instance.content_item.save()

        return super(ContentItemCRUDSerializer, self).update(instance, validated_data)

    class Meta:
        abstract = True


class DiscussionSerializer(serializers.ModelSerializer):
    content_item = FeedContentItemProfileSerializer()
    text_last_edited = serializers.DateTimeField(
        required=False,
        read_only=True
    )

    class Meta:
        model = Discussion
        fields = ('id', 'parent', 'order', 'content_item', 'text', 'text_last_edited')


cleaner = Cleaner(['a', 'p', 'abbr', 'acronym', 'b', 'code', 'pre', 'blockqote', 'span', 'sub', 'sup', 'code', 'em', 'i', 'ul', 'li', 'ol', 'strong', 'l', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'table', 'thead', 'caption', 'tbody', 'col', 'colgroup', 'tfoot', 'th', 'tr', 'td'], attributes={'*': ['style', 'alt', 'width', 'height'], 'a': ['href', 'title'], 'abbr': ['title'], 'acronym': ['title'], 'table': ['align', 'cellpadding', 'cellspacing'], 'th': ['scope'], 'colgroup': ['span'], 'caption': ['align']}, styles=['color', 'font-weight', 'text-decoration', 'background-color', 'color', 'text-align', 'border-style', 'border', 'border-width', 'border-color'])


class DiscussionCreateUpdateSerializer(ContentItemCRUDSerializer):
    content_item = FeedContentItemBasicSerializer(
        many=False,
        required=False
    )
    text_last_edited = serializers.DateTimeField(
        required=False,
        read_only=True
    )

    def save(self):
        text = self.validated_data['text']
        self.validated_data['text'] = cleaner.clean(text)
        super(DiscussionCreateUpdateSerializer, self).save()

    def create(self, validated_data):
        content_item_data = validated_data.pop('content_item')
        order = 0

        if validated_data.get('parent', 0):
            content_type = FeedContentItemType.objects.get(name=FeedContentItemType.POST)
            posts = Discussion.objects.filter(parent=validated_data['parent'])
            if posts.count() >= 1:
                order = posts.aggregate(Max('order'))['order__max'] + 1
            else:
                order = 1
        else:
            content_type = FeedContentItemType.objects.get(name=FeedContentItemType.TOPIC)

        content_item = FeedContentItem.objects.create(**content_item_data, content_type=content_type)

        discussion = Discussion.objects.create(**validated_data, content_item=content_item, order=order)
        # discussion.members.add(*member

        return discussion

    class Meta:
        model = Discussion
        fields = ('id', 'parent', 'order', 'content_item', 'text', 'text_last_edited')


class LinkSerializer(serializers.ModelSerializer):
    content_item = FeedContentItemProfileSerializer()

    class Meta:
        model = Link
        fields = ('id', 'content_item', 'link')

class BasicLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('id', 'link')


class LinkCreateUpdateSerializer(ContentItemCRUDSerializer):
    content_item = FeedContentItemBasicSerializer(
        many=False,
        required=False
    )

    def create(self, validated_data):
        content_item_data = validated_data.pop('content_item')

        content_type = FeedContentItemType.objects.get(name=FeedContentItemType.LINK)
        content_item = FeedContentItem.objects.create(**content_item_data, content_type=content_type)

        link = Link.objects.create(**validated_data, content_item=content_item)

        return link

    class Meta:
        model = Link
        fields = ('id', 'content_item', 'link')


class GroupForumSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        required=False
    )

    feed = FeedSerializer(
        read_only=False
    )

    is_local = serializers.SerializerMethodField()

    class Meta:
        model = GroupForum
        fields = ('id', 'name', 'image', 'description', 'feed', 'owner', 'is_restricted', 'is_local', 'members', 'rules')

    def get_is_local(self, instance):
        return instance.feed.places.count() != 0


class GroupForumCreateUpdateSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        required=False
    )

    feed = FeedCreateUpdateSerializer(
        read_only=False
    )

    def update(self, instance, validated_data):
        if 'feed' in validated_data:
            print(validated_data)
            for k,v in validated_data.pop('feed').items():
                setattr(instance.feed, k, v)

            instance.feed.save()

        return super(GroupForumCreateUpdateSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        feed_data = validated_data.pop('feed')
        interests = None
        content_types = None
        places = None
        print(feed_data)

        if 'interests' in feed_data:
            interests = feed_data.pop('interests')
        if 'content_types' in feed_data:
            content_types = feed_data.pop('content_types')
        if 'places' in feed_data:
            places = feed_data.pop('places')

        feed = Feed.objects.create(**feed_data)
        if interests:
            feed.interests.add(*interests)
        if content_types:
            feed.content_types.add(*content_types)
        if places:
            # NOTE only Places owned by this user can be added to the Group's feed
            feed.places.add(*places)

        stash = FeedContentStash.objects.create(name="Default", description="Stored content for this group")
        feed.stashes.add(*(stash,))

        members = validated_data.pop('members')
        group = GroupForum.objects.create(**validated_data, feed=feed)
        group.members.add(*members, group.owner)

        return group

    class Meta:
        model = GroupForum
        fields = ('id', 'name', 'image', 'description', 'feed', 'owner', 'is_restricted', 'members', 'rules')
