class InsufficientBalanceException(BaseException):
    def __init__(self, message="You don't have enough balance to proceed with this transaction", *args: object) -> None:
        self.message=message
        super().__init__(*args)