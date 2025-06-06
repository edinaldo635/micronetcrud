using System;
using System.Xml.Serialization;
using ApiProduto.Context;
using Lshopping.ApiProduto.Services;
using Lshopping.ApiProduto.Repositorio;

using Microsoft.EntityFrameworkCore;
using System.Reflection;


var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

//builder.Services.AddControllers();
// Add services to the container.
builder.Services.AddControllers();
   /* .AddJsonOptions(options =>
       {
           options.JsonSerializerOptions.ReferenceHandler =
               ReferenceHandler.IgnoreCycles;
       });*/


// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var connectionString =
    builder.Configuration.GetConnectionString("DefaultConnection")
        ?? throw new InvalidOperationException("Connection string"
        + "'DefaultConnection' not found.");

builder.Services.AddDbContext<MyDbContext>(options =>
    options.UseSqlServer(connectionString));

//builder.Services.AddAutoMapper(Assembly.GetEntryAssembly());

    
builder.Services.AddAutoMapper(AppDomain.CurrentDomain.GetAssemblies());
builder.Services.AddControllersWithViews();

// registros dos serviços no container IDI
builder.Services.AddScoped<IProdutoRepositorio, ProdutoRepositorio>();
builder.Services.AddScoped<ICategoriaRepositorio, CategoriaRepositorio>();
builder.Services.AddScoped<IProdutoService, ProdutoService>();
builder.Services.AddScoped<ICategoriaService, CategoriaService>();



var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.MapControllers();

app.Run();
