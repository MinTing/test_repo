/**
 * Comment form controller and view
 *
 * @class FormView
 * @extends Backbone.View
 * @author Bodnar Istvan <istvan@gawker.com>
 */
/*global Mustache, CommentView, CommentModel */
var FormView = Backbone.View.extend(
/** @lends FormView.prototype */
	{
		/**
		 * Html tag name of the container element that'll be created when initializing new instance.
		 * This container is then accessible via the this.el (native DOM node) or this.$el (jQuery node)
		 * variables.
		 * @type String
		 */

		tagName: 'div',
	
		/**
		 * CSS class name of the container element
		 * @type String
		 */
		className: 'commentform',
		
		/**
		 * The map of delegated event handlers
		 * @type Object
		 */
		events: {
			'click .submit': 'submit',
			'click .cancel': 'cancel'
		},
		
		/**
		 * View init method, subscribing to model events
		 */
		initialize: function () {
			console.log('this is formview initialize speaking');
			console.log(this.model.get('author'));
			this.model.on('change: author, text', this.updateFields, this);
			this.model.on('destroy', this.remove, this);
		},
		
		/**
		 * Render form element from a template using Mustache
		 * @returns {FormView} Returns the view instance itself, to allow chaining view commands.
		 */
		render: function () {
			var template = $('#form-template').text();
			var template_vars = {
				author: this.model.get('author'),
				text: this.model.get('text'),
			};
			var thismodel=this;
			if ($('.commentform').length==0)
			{
				this.$el.html(Mustache.to_html(template, template_vars));
				this.$el.find('.author')[0].placeholder=this.model.get('author');
				console.log(this.$el.find('.author')[0].placeholder);
				console.log(this.model.get('author'));
				this.$el.find('.author').bind('input', function(){
							thismodel.model.set({changed: 1});
				});
				this.$el.find('.text').bind('input', function(){
				thismodel.model.set({changed:1});
				});
				/*
					tried with jQuery UI Modal Form
					haven't got it working properly
				*/
				// this.$el.dialog(
				// 	{
				// 		title: 'New Comment',
				// 		height: 250,
				// 		width: 500,
				// 		draggable: true,
				// 		modal: true,
				// 		autoOpen: false,

				// 	});
				// element=this.$el;
				// element.dialog('open');
				// this.$el.bind('blur', function(){
				// 	console.log(this.html());
				// });
			}
			else
			{
				alert("only one comment form can be opened");
				return false;
			}
			return this;
		},
	
		/**
		 * Submit button click handler
		 * Sets new values from form on model, triggers a success event and cleans up the form
		 * @returns {Boolean} Returns false to stop propagation
		 */
	
	
		submit: function () {
			// set values from form on model
			this.model.set({
				author: this.$el.find('.author').val(),
				text: this.$el.find('.text').val(),
				changed: 0
			});

			
			// set an id if model was a new instance
			// note: this is usually done automatically when items are stored in an API
			if (this.model.isNew()) {
				this.model.id = Math.floor(Math.random() * 1000);
			}
			
			// trigger the 'success' event on form, with the returned model as the only parameter
			if (this.model.get('author')=='' || this.model.get('text')=='')
			{
				this.model.set({errormsg: true});
			}
			this.trigger('success', this.model);
			
			// remove form view from DOM and memory
			this.remove();
			return false;
		},
		/**
		* Cancel button click handler
		* Cleans up form view from DOM
		* @returns {Boolean} Returns false to stop propagation
		*/
		/*
		MinTing
		Function defined for confirmation before user canceling form input
		*/
		// Minting
		confirmation: function(){
			 if (this.model.get('changed'))
			{
				var a=window.confirm('Changes are made, are you sure you want to cancel?');
				return a;
				
			}
			else
			{
				return true;
			}
		},


		cancel: function () {
			// MinTing: modification for Question 1
			// clean up form
			var a=this.confirmation();
			console.log(a);
			if (a)
			{
				this.remove();
			}
			return false;
		},
		
		/**
		 * Update view if the model changes, helps keep two edit forms for the same model in sync
		 * @returns {Boolean} Returns false to stop propagation
		 */
		updateFields: function () {
			if (!this.model.get('changed'))
			{
				this.$el.find('.author').val(this.model.get('author'));
				this.$el.find('.text').val(this.model.get('text'));
			}
			return false;
		},
		
		/**
		 * Override the default view remove method with custom actions
		 */
		remove: function () {
			// unsubscribe from all model events with this context
			this.model.off(null, null, this);
			// delete container form DOM
			this.$el.remove();
			
			// call backbones default view remove method
			Backbone.View.prototype.remove.call(this);
		}
	}
);