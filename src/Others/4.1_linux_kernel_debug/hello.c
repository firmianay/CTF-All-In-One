#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>

static int hello_init(void)
{
        printk(KERN_ALERT "Hello module!\n");
        return 0;
}

static void hello_exit(void)
{
        printk(KERN_ALERT "Goodbye module!\n");
}

module_init(hello_init);
module_exit(hello_exit);

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("A simple module.");
