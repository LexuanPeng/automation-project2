from ..models import CryptoRewardRestService, BearerAuth


class AuthService(CryptoRewardRestService):
    def set_token(self, token: str):
        """Set authentication for this session."""
        self.session.auth = BearerAuth(token)
