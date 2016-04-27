(function(window, $){
    var CollectionIds = {
        render: function() {
           var self = this;
           var $select;
            
           if(!self.isSetProductCollectionPage())
               return;
            
           self.state = 'collapse';
           self.selectID = '#widget-set-collections';
            
           self.init(); 
           $select = self.createDropdown(); 
           $('.mws-form-item:eq(1)').before($select);
           self.renderContainerCategoryTree();
            
           $.getScript('https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.2/js/select2.min.js').done(function(script, textStatus){
               $select.select2({
                   tags: true
               });
           });
            
            $select.on('select2:select', function(e) {
               self.setCheckbox(e.params.data.id, true);
            }).on('select2:unselect', function(e) {
               self.setCheckbox(e.params.data.id, false);
            });
        },
        
        init: function(){
            var self = this;
            
            self.collectionsName = self.getCollectionsName();
            self.attachEventHeader();
            self.appendPlugins();
            self.setCss();
        },
        
        isSetProductCollectionPage: function() {
          return window.location.pathname.match(/products\/collection\/set/ig);  
        },
        
        setState: function(currentState) {
            this.state = currentState;
        },
        
        renderContainerCategoryTree: function() {
            var $container = $('<div></div>',{ id: 'widget-header-category-tree' });
            var $icon = $('<span></span>', { class: 'fa fa-angle-down' });
            var $header = $('<h4></h4>', { text: 'Category tree' });
            
            $icon.appendTo($container);
            $header.appendTo($container);
            
            $container.prependTo($('.collection-checkbox').closest('.mws-form-item'));
        },
        
        getCollectionsName: function(){
            var categoryLine = [];
            $('.mws-form-item').find('li').each(function(){
              var names = [];
              var collectionIds = [];
              var $parentsUl = $(this).parents('ul');
                
              if($(this).find('ul>li').length > 0)
                  return true;
                
              if($parentsUl.length > 1){
                $parentsUl.each(function(){
                  var $li = $(this).closest('li');
                  var $label = $li.find('>label');
                  var $checkbox = $li.find('>:checkbox');
                  if($label.text().length){
                    names.push($label.text());
                    collectionIds.push($checkbox.val());
                  }
                });
              }
                
              names.reverse().push($(this).find('>label').text());
              collectionIds.reverse().push($(this).find('>:checkbox').val());
              categoryLine.push({'name': names.join(' > '), 'ids': collectionIds, 'selected': $(this).find('>:checkbox').get(0).checked});
            });
            
            return categoryLine;
        },
        
        createDropdown: function(){
            var self = this;
            var $select = $('<select></select>',{ 'id': self.selectID, 'multiple': 'multiple'});
            
            for(var i = 0, max = self.collectionsName.length; i < max; i++){
                var collectionName = self.collectionsName[i];
                var $option = $('<option></option>',{
                    'text': collectionName.name,
                    'value': collectionName.ids,
                    'selected': collectionName.selected
                });
                
                $option.appendTo($select);
            }
            
            return $select;
        },
        
        appendPlugins: function() {
            $('head')
                .append('<link href="https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.2/css/select2.min.css" rel="stylesheet" />')
                .append('<link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.1/css/font-awesome.min.css" rel="stylesheet" />');
        },
        
        setCheckbox: function(list, isCheck) {
            var self = this;
            var collections = [];
            if(list.indexOf(',') === -1) {
                collections.push(list);
            } else {
                collections = list.split(',');
            }
            
            collections = collections.reverse();
            for(var i = 0, max = collections.length; i < max; i++){
                var $checkbox = $('input[value="'+ collections[i] +'"]');
                $checkbox.attr('checked',isCheck);
                if($checkbox.parent().siblings().find('input:checked').length)
                    break;
            }
        },
        
        attachEventHeader: function() {
            var self = this;
            var $collectionCheckbox = $('.collection-checkbox');
            $(document).on('click','#widget-header-category-tree', function() {
                if(self.state === 'collapse'){
                    self.setState('expand');
                    $(this).find('.fa').attr('class','fa fa-angle-up');
                    $collectionCheckbox.show();                    
                }else {
                    self.setState('collapse');
                    $(this).find('.fa').attr('class','fa fa-angle-down');
                    $collectionCheckbox.hide();      
                }
            });
        },
        
        setCss: function() {
            var css = [
                '.select2-selection.select2-selection--multiple::after { content: \'\'; clear: both; display: block; }',
                '.mws-form-row .select2-container--default .select2-selection--multiple .select2-selection__rendered { float: left; margin-bottom: 3px; }',
                '.mws-form-row .select2-container--default .select2-selection--multiple .select2-selection__choice { clear: both; padding: 4px 10px 2px; }',
                '.mws-form-row .select2-container--default .select2-selection--multiple .select2-selection__choice__remove { margin: 0 10px 0 -2px; vertical-align: middle; font-size: 20px; }',
                '.mws-form .mws-form-inline .select2 + .mws-form-item { border: 1px dashed #ddd; background-color: #fff; margin: 20px 0 0; }',
                '.mws-form-item > .collection-checkbox { overflow: hidden; margin-left: 0; display: none; border-top: 1px solid #ddd; padding: 20px 0 0 150px; }',
                '#widget-header-category-tree { padding: 10px 10px 5px; cursor: pointer; }',
                '#widget-header-category-tree .fa { margin: -5px 10px 0 0; font-size: 25px; vertical-align: middle; }',
                '#widget-header-category-tree > h4 { margin: 0; display: inline-block; }'
            ]
            
            $('style').last().append(css.join(''));
        }
    }
    
    CollectionIds.render();
})(this, jQuery);

/*
Exception: SyntaxError: missing ] after element list
@Scratchpad/2:108
*/
/*
Exception: SyntaxError: missing ) after argument list
@Scratchpad/2:40
*/