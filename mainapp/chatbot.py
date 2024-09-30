from openai import OpenAI
import os
from .models import *
from .context_generation import ContextGeneration
class Chatbot:
    
    client=OpenAI()
    assistant_id=os.environ.get('ASSISTANT_ID')
    
    def generateNormalGPTMessage(user_message):
        generate_message=Chatbot.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Be good"},
                {"role": "user", "content": f"{user_message}"}
            ]
        )
        return generate_message.choices[0].message.content
    
    def createOrGetThreadID(user_object,userChoice):
        # first check if there is any threads already created for the user_id
        try:
            user_thread=UserConversationThreads.objects.get(username=user_object)
            return user_thread.thread_id
        except UserConversationThreads.DoesNotExist:
            # if there is no thread for the user_id then create a new thread for the user_id
            # generate thread
            try:
                thread =  Chatbot.client.beta.threads.create()
            except Exception as e:
                print(e)
                return False
            try:
                new_thread_for_user=UserConversationThreads.objects.create(
                        username=user_object,
                        thread_id=thread.id
                )
                new_thread_for_user.save()
                return thread.id
            except Exception as e:
                print(e)
                return False
    
    def createMessageToThread(thread_id,user_message):
        posts_title,posts_text,post_comments=ContextGeneration.generateContext(message=user_message)
            
        user_message=user_message+f' cntxt- Some relevant reddit posts_list,post_texts_list, post_comments list related to the user text are given here: Posts:{posts_title}, Text in the Posts:{posts_text}, Corresponding comments with the post: {post_comments}'
        print(user_message)
        try:
            message=Chatbot.client.beta.threads.messages.create(
                thread_id=thread_id,
                role='user',
                content=user_message
            )
            return True
        except Exception as e:
            print(e)
            return False
    
    def createRunAndGenerateMessage(thread_id):
        try:
            run = Chatbot.client.beta.threads.runs.create_and_poll(
                thread_id=thread_id,
                assistant_id=Chatbot.assistant_id,
            )
            if(run.status=='completed'):
                response=Chatbot.client.beta.threads.messages.list(
                    thread_id=thread_id
                )
                assistant_message= response.data[0].content[0].text.value
                return assistant_message
            else:
                print(run.status)
                return False
        except:
            return False
            
    
    def generateAssistantMessages(user_message,userObject,userchoice):
        thread_id=Chatbot.createOrGetThreadID(userChoice=userchoice,user_object=userObject)
        if(thread_id==False):
            return False,"Can not generate Thread ID for the user"
        else:
            if(Chatbot.createMessageToThread(thread_id,user_message)):
                assistant_message=Chatbot.createRunAndGenerateMessage(thread_id)
                if(assistant_message==False):
                    return False,"Can not generate Assistant Message"
                else:
                    return True,assistant_message
            else:
                return False,"Can not create User Message"
    
    def getAllMessagesOfUser(userobject,userChoice):
        user_message_list=[]
        actual_user_message_list=[]
        assistant_message_list=[]
        if(userChoice):
            try:
                # get thread id of user
                thread=UserConversationThreads.objects.get(username=userobject)
                thread_messages = Chatbot.client.beta.threads.messages.list(thread_id=thread.thread_id)
                for message in (thread_messages.data):
                    if(message.role=='user'):
                        user_message_list.append(message.content[0].text.value)
                    elif(message.role=='assistant'):
                        assistant_message_list.append(message.content[0].text.value)
                for message in user_message_list:
                    actual_user_message_list.append(message.split('cntxt-')[0])
                    
                return True,actual_user_message_list[::-1],assistant_message_list[::-1],"Previous history retrieved!"
            except UserConversationThreads.DoesNotExist:
                return True,actual_user_message_list[::-1],assistant_message_list[::-1],"No previous chat history was found!"
            except Exception as e:
                print(e)
                return False,user_message_list,assistant_message_list,"Something went wrong while fetching messages"
        else:
            # As im storing threads of the user, this is the time where i delete the record
            # and then create a new one with the new thread id
            try:
                thread = UserConversationThreads.objects.get(username=userobject)
                thread.delete()
            except UserConversationThreads.DoesNotExist:
                pass
            return True,user_message_list,assistant_message_list,"No history of chat for the user"