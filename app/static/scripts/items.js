'use strict';

$(document).ready(function(){
    checkDocumentVisibility(checkLogin);//check document visibility in order to confirm user's log in status
    $("#createItem").click(function(){
        $("#itemsListDiv").toggleClass("col-sm-8", "col-sm-12");
        $("#createNewItemDiv").toggleClass('hidden');
        $("#itemdescriptionunit").focus();
    });

    $("#createSubcategory").click(function(){
        $("#itemsListDiv").toggleClass("col-sm-8", "col-sm-12");
        $("#createNewSubcategoryDiv").toggleClass('hidden');
        $("#itemdescriptionunit").focus();
    });

    $("#createCategory").click(function(){
        $("#itemsListDiv").toggleClass("col-sm-8", "col-sm-12");
        $("#createNewCategoryDiv").toggleClass('hidden');
        $("#itemdescriptionunit").focus();
    });
    
    
    $(".cancelAddItem").click(function(){
        //reset and hide the form
        document.getElementById("addNewItemForm").reset();//reset the form
        $("#createNewItemDiv").addClass('hidden');//hide the form
        $("#itemsListDiv").attr('class', "col-sm-12");//make the table span the whole div
    });

    $(".cancelAddSubcategory").click(function(){
        //reset and hide the form
        document.getElementById("addNewSubcategoryForm").reset();//reset the form
        $("#createNewSubcategoryDiv").addClass('hidden');//hide the form
        $("#itemsListDiv").attr('class', "col-sm-12");//make the table span the whole div
    });

    $(".cancelAddCategory").click(function(){
        //reset and hide the form
        document.getElementById("addNewCategoryForm").reset();//reset the form
        $("#createNewCategoryDiv").addClass('hidden');//hide the form
        $("#itemsListDiv").attr('class', "col-sm-12");//make the table span the whole div
    });
    
    //handles the submission of adding new item
    $("#itemsListTable").on('click', ".editItem", function(e){
        $("#updateCategoryModal").modal('show');
    });

    $("#itemsListTable").on('click', ".editItem", function(e){
        $("#updateSubcategoryModal").modal('show');
    });
    
    //trigers the modal to update stock
    $("#itemsListTable").on('click', '.updateStock', function(){
        $("#updateCategoryModal").modal('show');
    });
});
