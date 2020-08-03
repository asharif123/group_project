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

})