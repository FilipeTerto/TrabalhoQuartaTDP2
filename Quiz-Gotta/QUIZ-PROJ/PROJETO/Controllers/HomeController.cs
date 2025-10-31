using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using Quiz_Gotta.Models;


namespace Quiz_Gotta.Controllers
{
    public class HomeController : Controller
    {
        // Rota principal do quiz
        public IActionResult Index()
        {
            return View();
        }
    }
}
