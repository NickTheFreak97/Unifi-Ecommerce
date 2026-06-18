from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class JWTSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        fields = super().validate(attrs)

        fields["username"] = self.user.get_username()

        return fields