const TEMPLATES_LOCATION = '/static/admin_site/templates/';
const STATIC_LOCATION = '/static/'
const EXTRA_TEMPLATE_CONTEXT = {
	'static':STATIC_LOCATION,
	'carts_length':carts_length
}
const API_URL = '/api/'
const REFRESH_INTERVAL = 120000 //In microseconds

String.prototype.format = function() {
	a = this;
	for (k in arguments) {
		a = a.replace("{" + k + "}", arguments[k])
	}
	return a
}

var carts_length = 0;

class Shortcuts{
	static reportError(error_text){
		var error_id = Math.random().toString(36).substring(7);
		template_loader.load('error_template.hbs', {'error_message':error_text, 'error_id':error_id}, function(html){
			$('#top-notification-container').prepend(html);
			$("#error-toast-{0}".format(error_id)).toast('show');
		})
	}

	static reportSuccess(success_message){
		var success_id = Math.random().toString(36).substring(7);
		template_loader.load('success_template.hbs', {'success_message':success_message, 'success_id':success_id}, function(html){
			$('#top-notification-container').prepend(html);
			$('#success-toast-{0}'.format(success_id)).toast('show');
		})
	}
}


class Template{
	constructor(name){
		this.name = name;
	}

	setValue(html){
		this.html = Handlebars.compile(html);
	}

	compile(data){
		return this.html(data,{allowedProtoProperties: {name: true}});
	}

	getValue(){
		return this.html;
	}
}


class TemplateLoader{

	constructor(template_location, extra_context){
		this.template_location = template_location;
		this.cache = [];
		this.extra_context = extra_context;
	}

	isCached(template){
		return (this.cache.filter(t => t.name == template.name).length)
	}

	getCached(template){
		return this.cache.filter(t => t.name == template.name)[0];
	}

	addToCache(template){
		this.cache.push(template);
	}

	async getTemplate(template_name){
		var template = new Template(template_name);

		if(this.isCached(template)){
			return this.getCached(template);
		}
		await $.get(this.template_location + template_name, function(template_content){
			template.setValue(template_content);
		});
		this.addToCache(template);
		return template;
	}

	async load(template_name, data, success_function){
		var template = await this.getTemplate(template_name);
		data['context'] = this.extra_context;
		success_function(template.compile(data));
	}

}


class Cart{

	constructor(data){
		this.data = data;
		this.data['length'] = this.data.orders.length
	}

	async render(){
		await template_loader.load('cart_template.hbs', this.data, function(html){
			Cart.CONTAINER.append(html);
		});
		carts_length++;
	}

	static emptyContainer(){
		Cart.CONTAINER.empty();
		carts_length=0;
		$('.modal-backdrop').remove();
	}

	static setLengthView(length){
		Cart.LENGTH_CONTAINER.html(length);
	}
	
	static async fetchCarts(){
		console.log('[+]Fetching Carts');
		await $.ajax({
			url: API_URL + 'core/carts/',
			data: {
				new: 1
			},
			success: async function(data){
				Cart.setLengthView(data.length)
				data.forEach(async element =>  {
					Cart.emptyContainer();
					let cart = new Cart(element);
					await cart.render();
				});
				console.log(data);
			}
		});
	}

	static async startFetchLoop(){
		Cart.fetchCarts();
		setInterval(Cart.fetchCarts, REFRESH_INTERVAL);
	}
}

Cart.CONTAINER = $("#orders-container");
Cart.LENGTH_CONTAINER = $("#orders-length");

function init(){
	console.log('[+]Init running...')
	$(document).ready(async function(){
		console.log('[+]Document ready')
		template_loader = new TemplateLoader(TEMPLATES_LOCATION, EXTRA_TEMPLATE_CONTEXT);
		console.log('[+]Template Loader Ready.')
		Cart.startFetchLoop();
	});
}

init();