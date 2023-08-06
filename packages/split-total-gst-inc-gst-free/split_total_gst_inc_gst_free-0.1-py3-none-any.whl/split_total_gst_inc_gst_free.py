#!/usr/bin/env python
# coding: utf-8

# In[50]:


from money2float import money


# In[60]:


def split_totals(net_total, gst_total, gross_total, gst_rate):
    gst_incl = {}
    gst_free = {}
    new_gstincl_net = gst_total * 10
    new_gstfree_net = net_total - new_gstincl_net
    new_gstincl_gross = new_gstincl_net + gst_total
    new_gstfree_gross = gross_total - new_gstincl_gross

    gst_incl["net_total"] = money(new_gstincl_net)
    gst_incl["gst_total"] = gst_total
    gst_incl["gross_total"] = money(new_gstincl_gross)

    gst_free["net_total"] = new_gstfree_net
    gst_free["gst_total"] = 0
    gst_free["gross_total"] = money(new_gstfree_gross)
    lines = {"gst_incl": gst_incl, "gst_free": gst_free}
    return lines


# In[ ]:
