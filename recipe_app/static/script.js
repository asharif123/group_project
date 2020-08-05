$(document).ready(function(){
    $('#recipe_filter').submit(function(e){
        console.log('PASS!')
        e.preventDefault()
        $.ajax({
            url: '/recipe/filter',
            method: 'post',
            data: $(this).serialize(),

            success: function(serverResponse){
                console.log(serverResponse)
            // replace everything in noteboard with the response we get (ex: serverResponse -> file we're rendring) using .html replaces html in that noteboard section

                $('.welcome').html(serverResponse)
                }

                

        })
    })

    $('#dessert_filter').submit(function(e){
        console.log('PASS!')
        e.preventDefault()
        $.ajax({
            url: '/dessert/filter',
            method: 'post',
            data: $(this).serialize(),

            success: function(serverResponse){
                console.log(serverResponse)
            // replace everything in noteboard with the response we get (ex: serverResponse -> file we're rendring) using .html replaces html in that noteboard section

                $('.dessert').html(serverResponse)
                }

                

        })
    })

    $('#review').submit(function(e){
        e.preventDefault()
        $.ajax({
            url: "/review/add",
            method: "POST",
            data: $(this).serialize(),
            success: function(serverResponse){
                console.log(serverResponse)
                $('#reviews').html(serverResponse);
                // reset everything in the form action having id review
                $('#review').trigger('reset');
            
            }
        })
    })

    $('#dessert_review').submit(function(e){
        e.preventDefault()
        $.ajax({
            url: "/dessert/review/add",
            method: "POST",
            data: $(this).serialize(),
            success: function(serverResponse){
                console.log(serverResponse)
                $('#reviews').html(serverResponse);
                // resets everything in the form!
                $('#dessert_review').trigger('reset');
            
            }
        })
    })


// .on pays attention to everything happening in ajax, everytime delete review in AJAX
// .submit page loads and looks at it, when replaced, jQuery no longer pays attention
// .on sees any new info or content being put in
// form.delete_review specifices exactly what we are listening to

    $('#reviews').on('submit','form.delete_review',function(e){
        e.preventDefault()
        // console.log($(this).serialize())
        // delete THIS review
        // var review = $(this).attr('review')
        $.ajax({
            url: "/review/delete",
            method: "POST",
            data: $(this).serialize(),
            success: function(serverResponse){
                console.log(serverResponse)
                $('#reviews').html(serverResponse)
                // $('.content').trigger('reset');

            
            }
        })
    })


})