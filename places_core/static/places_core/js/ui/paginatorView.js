//
// paginatorView.js
// ================
// Simple Backbone view to display navigation for PageableCollection.
//
define(['jquery',
        'underscore',
        'backbone'],

function ($, _, Backbone) {
    
    "use strict";
    
    var PaginatorView = Backbone.View.extend({
        
        tagName: 'div',
        
        className: 'paginator',
        
        template: _.template($('#paginator-tpl').html()),
        
        events: {
            'click .first-page': 'firstPage',
            'click .last-page': 'lastPage',
            'click .next-page': 'nextPage',
            'click .prev-page': 'prevPage'
        },
        
        initialize: function (collection) {
            this.collection = collection;
            this.listenTo(this.collection, 'sync', this.render);
        },
        
        render: function () {
            var self = this;
            self.$el.empty();
            if (this.collection.state.totalPages > 1) {
                this.$el.html(this.template(this.collection.state));
                this.$el.find('.page').on('click', function (e) {
                    self.getPage($(this).attr('data-index'));
                });
            }
            return this;
        },
        
        getPage: function (idx) {
            this.collection.getPage(parseInt(idx, 10));
            this.setCounter();
        },
        
        firstPage: function () {
            this.collection.getFirstPage();
            this.setCounter();
        },
        
        lastPage: function () {
            this.collection.getLastPage();
            this.setCounter();
        },
        
        nextPage: function () {
            if (this.collection.hasNextPage()) {
                this.collection.getNextPage();
                this.setCounter();
            }
        },
        
        prevPage: function () {
            if (this.collection.hasPreviousPage()) {
                this.collection.getPreviousPage();
                this.setCounter();
            }
        },
        
        setCounter: function () {
            this.$el.find('.current-page')
                .text(this.collection.state.currentPage);
        }
    });
    
    return PaginatorView;
});