from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Account, Transaction
from .serializers import TransactionSerializer, AccountSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView


user = get_user_model()

class signupView(APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request, format=None):
        data = self.request.data
        email = data["email"]
        username = data["username"]
        balance = data["balance"]
        pass1 = data["pass1"]
        pass2 = data["pass2"]
        print("recieved data")
        if pass1 == pass2:
            if user.objects.filter(email=email).exists():
                return Response({"message": "Email Address Already Exists"})
            else:
                print("email is fine")
                if len(pass1)<6:
                    return Response({"message": "Password Must Have Atleast 6 Characters"})
                else:
                    print("pass is fine")
                    USER = user.objects.create_user(email=email, password=pass1, username=username, balance=balance) 
                    USER.save()
                    print("user saved")
                    return Response({"message": "ACCOUNT CREATED SUCCESSFULLY"})
        else:
            return Response({"message": "Passwords Don't Match"})




#   THIS VIEW RETRIEVES A LIST OF ALL THE TRANSACTIONS
class transactionLISTView(ListAPIView):                                     ##############################################
    permission_classes = (permissions.AllowAny, )                           ## **REMOVE "permissions.AllowAny"          ##
    queryset = Transaction.objects.order_by("-id")                          ##  FROM ALL THE VIEWS FOR AUTHENTICATION   ##
    serializer_class = TransactionSerializer                                ##  REQUIREMENT AND SECURITY**              ##
    pagination_class = None                                                 ##############################################
    


#   THIS VIEW RETRIEVES A LIST OF ALL THE USERS
class usersListView(ListAPIView):
    permission_classes = (permissions.AllowAny, )
    queryset = Account.objects.order_by("username")
    serializer_class = AccountSerializer
    pagination_class = None



#   THIS VIEW MANAGES TRANSACTIONS BETWEEM USERS
class transactionView(APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request, format=None):
        data = self.request.data
        senderEmail = data["senderEmail"]
        recieverEmail = data["recieverEmail"]
        transferredAmount = data["transferredAmount"]
        print("recieved data")
        sender = Account.objects.get(email=senderEmail)
        reciever = Account.objects.get(email=recieverEmail)
        if sender.balance < int(transferredAmount):
            return Response({"message": "Not Enough Balance"})
        sender.balance -= int(transferredAmount)
        reciever.balance += int(transferredAmount)
        print("sender is : ", sender)
        print("reciever is : ", reciever)
        print("transferred Amount is : ", transferredAmount)
        TRANSACTION = Transaction.objects.create(sender=sender, reciever=reciever, transferredAmount=transferredAmount) 
        TRANSACTION.save()
        sender.save()
        reciever.save()
        print("transaction saved")
        return Response({"message": "Transaction Successful"})