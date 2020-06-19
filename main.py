from flask import Flask, render_template,jsonify, abort,request, redirect, url_for, flash, make_response, request
from flask_script import  Command, Shell
from flask_httpauth import HTTPBasicAuth
from forms import ContactForm
import datetime
import json 

app = Flask(__name__)
auth = HTTPBasicAuth()
app.debug = True
app.config['SECRET_KEY'] = 'KostianTheBest'
app.config['JSON_AS_ASCII'] = False


#доступ к api только для админа
@auth.get_password
def get_password(username):
    if username == 'admin Kostia':
        return 'ilove(no)fam'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'You motherfucker, come on you little ass… fuck with me, eh? You fucking little asshole, dickhead cocksucker…You fuckin come on, come fuck with me! I will get your ass, you jerk! Oh, you fuckhead motherfucker! Fuck all you and your family! Come on, you cocksucker, slime bucket, shitface turdball! Come on, you scum sucker, you fucking with me? Come on, you asshole!!!'}), 401)

#api со всем сообщениями
@app.route('/api/v1.0/messages', methods=['GET'])
@auth.login_required
def get_messages():
	with open('messages.json', encoding='utf-8') as json_file:
	    data = json.load(json_file)
	    return jsonify(data)
    


#api конкретного сообщения
@app.route('/api/v1.0/messages/<message_time>', methods=['GET'])
@auth.login_required
def get_one_message(message_time):
	with open('messages.json', encoding='utf-8') as json_file:
	    data = json.load(json_file)

	    message = list(filter(lambda t: t['Time'] == message_time, data))
	    if len(message) == 0:
	        abort(404)
	    return jsonify(message[0]), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#удаление api (пока что не работает и скорее всего не будет)
@app.route('/api/v1.0/messages/<message_time>', methods=['DELETE'])
@auth.login_required
def delete_message(message_time):
	with open('messages.json', encoding='utf-8') as json_file:
	    data = json.load(json_file)
	    message = filter(lambda t: t['Time'] == message_time, data)
	    if len(message) == 0:
	        abort(404)
	    data.remove(message[0])
	    return jsonify({'result': True})




#контактная страница с записью сообщения в api
@app.route('/contacts_page', methods=['get', 'post'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        current_time=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        message={
        	'Time':current_time,
        	'Name':name,
        	'Message':message,
        	'Email':email,
        }

        try:
        	with open('messages.json', 'r', encoding='utf-8') as json_file:
        		data = json.load(json_file)
        except:
        	data=[]

        data.append(message)


        with open('messages.json', 'w', encoding='utf-8') as json_file:
        	json.dump(data, json_file, ensure_ascii=False, indent=4)

       # flash('Повідомлення успішно відправлене');
        return redirect(url_for('contact'))

    return render_template('contacts_page.html', form=form)

#оставшиеся страницы
@app.route('/admin')
@auth.login_required
def admin_control():
    return render_template('admin.html')


  	
@app.route('/vstup_bakalavrat')
def vstup_bakalavrat():
    return render_template('vstup_bakalavrat.html')

@app.route('/rozklad')
def rozklad():
    return render_template('rozklad.html')

@app.route('/international_activity')
def international_activity():
    return render_template('international_activity.html')





if __name__ == "__main__":
    app.run()
