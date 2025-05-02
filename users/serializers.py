from rest_framework import serializers
from users.models import CustomUser, UserProfile, MilitaryRank
from location.models import School

class MilitaryRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = MilitaryRank
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'full_name', 'role', 'is_active', 'is_staff', 'date_joined']
        extra_kwargs = {
            'username': {'required': True, 'min_length': 4},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def get_full_name(self, obj):
        return obj.get_full_name()

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Bu username allaqachon mavjud.")
        if not value.isalnum():
            raise serializers.ValidationError("Username faqat harf va raqamlardan iborat bo‘lishi kerak.")
        return value

    def validate_role(self, value):
        if value not in [role[0] for role in CustomUser._meta.get_field('role').choices]:
            raise serializers.ValidationError("Noto‘g‘ri rol tanlandi.")
        return value

    def validate_username(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("Username faqat harf va raqamlardan iborat bo‘lishi kerak.")
        if len(value) < 4:
            raise serializers.ValidationError("Username kamida 4 belgidan iborat bo‘lishi kerak.")
        return value

    def validate_first_name(self, value):
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("Ismda raqam bo‘lishi mumkin emas.")
        return value

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'role', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True, source='user')
    military_rank = MilitaryRankSerializer(read_only=True)
    military_rank_id = serializers.PrimaryKeyRelatedField(queryset=MilitaryRank.objects.all(), write_only=True, source='military_rank')
    school = serializers.StringRelatedField(read_only=True)
    school_id = serializers.PrimaryKeyRelatedField(queryset=School.objects.all(), write_only=True, source='school')

    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'user_id', 'middle_name', 'school', 'school_id',
            'military_rank', 'military_rank_id', 'jshir', 'department',
            'birth_date', 'birth_place', 'phone', 'passport_series', 'profile_image', 'created_at'
        ]
        extra_kwargs = {
            'middle_name': {'help_text': "Otasining ismi", 'required': False},
            'jshir': {'help_text': "JShShIR"},
            'department': {'help_text': "Bo‘lim nomi"},
            'birth_date': {'help_text': "Tug‘ilgan sana"},
            'birth_place': {'help_text': "Tug‘ilgan joy"},
            'phone': {'help_text': "Telefon raqam"},
            'passport_series': {'help_text': "Pasport seriyasi"},
        }

    def create(self, validated_data):
        return UserProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def validate_jshir(self, value):
        if value and (len(value) != 14 or not value.isdigit()):
            raise serializers.ValidationError("JSHIR 14 xonali raqam bo‘lishi kerak.")
        return value

    def validate_birth_date(self, value):
        from datetime import date
        if value and value > date.today():
            raise serializers.ValidationError("Tug‘ilgan sana kelajakda bo‘lishi mumkin emas.")
        return value

    def validate(self, data):
        # Misol: passport_series faqat 2 harf + 7 raqam bo‘lishi kerak (masalan: AA1234567)
        series = data.get('passport_series')
        if series:
            import re
            if not re.match(r'^[A-Z]{2}\d{7}$', series.upper()):
                raise serializers.ValidationError({
                    'passport_series': "Pasport seriyasi 2 harf va 7 raqamdan iborat bo‘lishi kerak. (Masalan: AB1234567)"
                })

        return data

    def validate_phone(self, value):
        import re
        if value and not re.match(r'^\+998\d{9}$', value):
            raise serializers.ValidationError("Telefon raqam +998XXXXXXXXX formatida bo‘lishi kerak.")
        return value

    def validate_middle_name(self, value):
        if value and any(char.isdigit() for char in value):
            raise serializers.ValidationError("Otasining ismida raqam bo‘lishi mumkin emas.")
        return value
