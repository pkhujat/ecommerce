$(document).ready(function (e) {

    if (user == 'AnonymousUser'){
      $("#logout").addClass('hidden')
      $("#login").removeClass('hidden')
    }
    else{
      $("#logout").removeClass('hidden')
      $("#login").addClass('hidden')
    }

    $("#check_cart").on('click',function(){
        alert("Please add item to cart");
    });

    $(".update_cart").on('click', function(){
       var product_id  = this.dataset.product;
       var action = this.dataset.action;
      // alert(user);
       if (user == 'AnonymousUser')
       {
           console.log('User Is not authenticated');
           alert("Please Login")
       }
       else{
           console.log('User Is authorised');
           updateUserOrder(product_id,action);
       }
     });

     $("#logout").on('click',function(){
         console.log('Logout Clicked')
         if (user != 'AnonymousUser')
         {
             logoutUser();
         }
     })
     
     //$('.qololbl').trigger('click');

     $("#btnsearch").on('click',function(){
        var form = document.getElementById('form')
		form.addEventListener('submit', function(e){
	    	e.preventDefault()
	    	console.log('Form Submitted...')
	    })
        var searchterm = $("#searchprod").val();
        filterProduct(searchterm);
    
        
     })
});

function updateUserOrder(productId,action){
    console.log('User is authenticated, sending data...')

    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        }, 
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) => {
       return response.json();
    })
    .then((data) => {
        console.log(data);
        location.reload()
    });

}

function logoutUser(){
    console.log('Log out user process...')

    var url = '/logout_user/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        }, 
        //body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) => {
       return response.json();
    })
    .then((data) => {
        console.log(data);
        location.reload()
    });

}

function filterProduct(searchtearm){
    console.log('User is authenticated, sending data...')

    var url = '/filter_store/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        }, 
        body:JSON.stringify({'searchtearm':searchtearm})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log(data);
        window.location.href = "{% url 'store' %}"
       
    });

}