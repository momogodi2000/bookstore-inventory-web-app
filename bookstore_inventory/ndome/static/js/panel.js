    $(document).ready(function(){
        $('.btn').hover(function(){
            $(this).addClass('animated pulse');
        }, function(){
            $(this).removeClass('animated pulse');
        });
    });



    // Example animation script (replace with actual payment gateway integration)
document.getElementById('pay-button').addEventListener('click', function() {
    alert('Redirecting to payment gateway...');
    // Add animation or loading state here
});


$(document).ready(function() {
    $('.btn').hide().fadeIn(1000);
});
